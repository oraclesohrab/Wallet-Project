import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Wallet, Currency
from .key_generator import KeyGenerator
from .bitcoin import BitcoinWallet
from .ethereum import EthereumWallet
from cryptoaddress import BitcoinAddress, EthereumAddress
# Create your views here.


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_wallet_view(request):

	if request.method == 'POST':
		data={
			"error": None,
			"is_success": False,
			"address": None,
			"validation_message": None
		}
		# Checking if the Coin is exist
		try:
			coin = Currency.objects.get(abbr=request.data['coin'].upper())
		except Currency.DoesNotExist:
			data['error'] = f"Coin '{request.data['coin']}' does not exist!!!"
			return Response(data)
		# Check if user have wallet for the coin

		try: 
			wallet = Wallet.objects.get(user=request.user, currency=coin)
		except Wallet.DoesNotExist:
			wallet = None

		if not wallet:
			key_generation = KeyGenerator()
			private_key = key_generation.generate_key()
			if coin.abbr == "BTC":
				bitcoin_wallet = BitcoinWallet
				wallet_data = bitcoin_wallet.generate_wallet(private_key)
				#Validate the address
				try:
					BitcoinAddress(wallet_data['address'])
					data['validation_message'] = 'The address is valid.'
				except ValueError as e:
					data['validation_message'] = 'The address is invalid.'
					return Response(data)
			elif coin.abbr == "ETC":
				ethereum_wallet = EthereumWallet
				wallet_data = ethereum_wallet.generate_wallet(private_key)
				#Validate the address
				try:
					EthereumAddress(wallet_data['address'])
					data['validation_message'] = 'The address is valid.'
				except ValueError:
					data['validation_message'] = 'The address is invalid.'
					return Response(data)

			address = wallet_data['address']
			data['address'] = address
			new_wallet = Wallet.objects.create(user=request.user, currency=coin)
			new_wallet.address = wallet_data['address']
			new_wallet.public_key = wallet_data['public_key']
			new_wallet.save()
			
			backup_file = {
				"private_key": private_key,
				"public_key": wallet_data['public_key'].decode("utf-8"),
				"address": wallet_data['address']
			}
			
			""" BACKING UP THE WALLET INFO AND PRIVATE KEY """
			with open(f"{coin.abbr}-{request.user.id}.json", "w") as write_file:
				json.dump(backup_file, write_file)
			""" END WRITING """

			

		else:
			address = wallet.address
			data['address'] = address
			data['validation_message'] = 'The address is already validated and is valid.'
		
		

		data['is_success'] = True
		return Response(data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def wallet_list_view(request):

	if request.method == 'GET':
		data={
			"error": None,
			"is_success": False,
			"wallets": list()
		}
		wallets = Wallet.objects.filter(user=request.user)
		if len(wallets) == 0 :
			data['error'] = "You don't have any wallet yet!!!"
			return Response(data)
		wallet_list = list()
		for wallet in wallets:
			wallet_info = {
				"id": wallet.id,
				"currency": wallet.currency.name,
				"address": wallet.address,
				"public_key": wallet.public_key
			}
			wallet_list.append(wallet_info)
		
		data['wallets'] = wallet_list
		data['is_success'] = True
		return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def get_wallet_view(request):

	if request.method == 'POST':
		data={
			"error": None,
			"is_success": False,
			"wallet": dict()
		}
		try:
			wallet = Wallet.objects.get(user=request.user, id=request.data['id'])
		except Wallet.DoesNotExist:
			data['error'] = f"You don't have wallet with id: {request.data['id']}!!!"
			return Response(data)
		data['wallet'] = {
				"currency": wallet.currency.name,
				"address": wallet.address,
				"public_key": wallet.public_key
			}
		data['is_success'] = True
		return Response(data)


@api_view(['GET', ])
@permission_classes((IsAdminUser,))
def all_wallet_list_view(request):

	if request.method == 'GET':
		data={
			"error": None,
			"is_success": False,
			"wallets": list()
		}
		wallets = Wallet.objects.all()
		if len(wallets) == 0 :
			data['error'] = "There are not any wallet yet!!!"
			return Response(data)
		wallet_list = list()
		for wallet in wallets:
			wallet_info = {
				"id": wallet.id,
				"user": wallet.user.username,
				"currency": wallet.currency.name,
				"address": wallet.address,
				"public_key": wallet.public_key
			}
			wallet_list.append(wallet_info)
		
		data['wallets'] = wallet_list
		data['is_success'] = True
		return Response(data)


@api_view(['POST', ])
@permission_classes((IsAdminUser,))
def get_wallet_admin_view(request):

	if request.method == 'POST':
		data={
			"error": None,
			"is_success": False,
			"wallet": dict()
		}
		try:
			wallet = Wallet.objects.get(id=request.data['id'])
		except Wallet.DoesNotExist:
			data['error'] = f"Wallet with id: {request.data['id']} does not exist!!!"
			return Response(data)
		data['wallet'] = {
				"user": wallet.user.username,
				"currency": wallet.currency.name,
				"address": wallet.address,
				"public_key": wallet.public_key
			}
		data['is_success'] = True
		return Response(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def get_backup_view(request):

	if request.method == 'POST':
		data={
			"error": None,
			"is_success": False,
			"wallet": dict()
		}

		with open(f"{request.data['coin'].upper()}-{request.user.id}.json", "r") as read_file:
			file = json.load(read_file)
		if file['public_key'] != request.data['public_key']:
			data['error'] = "The public key you entered is incorrect. \n Please enter a correct key."
			return Response(data)
		try:
			Wallet.objects.get(user=request.user, public_key=request.data['public_key'].encode())
		except Wallet.DoesNotExist:
			new_wallet = Wallet.objects.create(user=request.user, currency=Currency.objects.get(abbr=request.data['coin']))
			new_wallet.address = file['address']
			new_wallet.public_key = file['public_key']
			new_wallet.save()
			
		data['wallet'] = file
		data['is_success'] = True
		return Response(data)