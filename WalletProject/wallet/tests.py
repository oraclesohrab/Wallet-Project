from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from account.models import User
from .models import Wallet, Currency

class APITests(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create(username="testuser",
                                               email="test@gmail.com",
                                               password="12345678")
        self.client_user.save()
        self.token = Token.objects.get(user=self.client_user)
        self.bitcoin = Currency.objects.create(name="Bitcoin", abbr="BTC")
        self.ethereum = Currency.objects.create(name="Ethereum", abbr="ETC")
        self.admin_user = User.objects.create(username="adminuser",
                                               email="admin@gmail.com",
                                               password="12345678")
        self.admin_user.is_admin=True
        self.admin_user.is_superuser=True
        self.admin_user.is_staff=True
        self.admin_user.save()
        self.admin_token = Token.objects.get(user=self.admin_user)
    
    def test_5_create_wallet_success(self):
        print("Test create wallet Success")
        create_wallet_url = reverse('create_wallet')
        data = {
            "coin": "BTC"
        }
        header = {'HTTP_AUTHORIZATION': f"Token {self.token}"}
        response = self.client.post(create_wallet_url, data, **header)
        response = response.json()
        self.assertEqual(response['validation_message'], 'The address is valid.')
        self.assertTrue(response['is_success'])
        self.assertEqual(response['error'], None)
        print("Success!!!")


    def test_6_wallet_list_success(self):
        print("Test wallet list Success")
        wallet_list_url = reverse('user_wallets')
        create_wallet_url = reverse('create_wallet')
        header = {'HTTP_AUTHORIZATION': f"Token {self.token}"}
        self.client.post(create_wallet_url, {"coin":"btc"}, **header)
        self.client.post(create_wallet_url, {"coin":"etc"}, **header)
        response = self.client.get(wallet_list_url, **header)
        response = response.json()
        self.assertTrue(response['is_success'])
        self.assertEqual(response['error'], None)
        print("Success!!!")


    def test_7_get_wallet_success(self):
        print("Test get user wallet Success")
        get_wallet_url = reverse('get_wallet')
        create_wallet_url = reverse('create_wallet')
        header = {'HTTP_AUTHORIZATION': f"Token {self.token}"}
        self.client.post(create_wallet_url, {"coin":"btc"}, **header)
        wallet = Wallet.objects.get(user=self.client_user, currency=self.bitcoin)
        data = {"id": wallet.id}
        response = self.client.post(get_wallet_url, data, **header)
        response = response.json()
        self.assertTrue(response['is_success'])
        self.assertEqual(response['error'], None)
        print("Success!!!")
    

    def test_8_add_wallet_list_success(self):
        print("Test get all wallets admin Success")
        all_wallet_url = reverse('all_wallets')
        create_wallet_url = reverse('create_wallet')
        header = {'HTTP_AUTHORIZATION': f"Token {self.token}"}
        self.client.post(create_wallet_url, {"coin":"btc"}, **header)
        self.client.post(create_wallet_url, {"coin":"etc"}, **header)
        header = {'HTTP_AUTHORIZATION': f"Token {self.admin_token}"}
        response = self.client.get(all_wallet_url, **header)
        response = response.json()
        self.assertTrue(response['is_success'])
        self.assertEqual(response['error'], None)
        print("Success!!!")
    

    def test_9_get_wallet_admin_success(self):
        print("Test get admin wallet Success")
        get_admin_wallet_url = reverse('admin_get_wallet')
        create_wallet_url = reverse('create_wallet')
        header = {'HTTP_AUTHORIZATION': f"Token {self.token}"}
        self.client.post(create_wallet_url, {"coin":"btc"}, **header)
        wallet = Wallet.objects.get(user=self.client_user, currency=self.bitcoin)
        data = {"id": wallet.id}
        header = {'HTTP_AUTHORIZATION': f"Token {self.admin_token}"}
        response = self.client.post(get_admin_wallet_url, data, **header)
        response = response.json()
        self.assertTrue(response['is_success'])
        self.assertEqual(response['error'], None)
        print("Success!!!")