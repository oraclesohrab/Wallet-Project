# Wallet-Project
Technical Challenge for Zeply
Programmin language : Python 3.8
Framework : Django-restframework

Note: I wrote this task based on user so users can see their own wallet and addresses. 
-All the addresses generated will validate.
-For getting the whole addresses(wallets) list you should use : "/wallet/all_wallets_list/" endpoint with admin user token.
-For getting specific address(wallet) without checking the owner you should use : "/wallet/admin_get_wallet/" endpoint with admin user token.
-For retreive backup data for wallet or private key you should use : "/wallet/get_backup/" endpoint with user public_key and currency abbrevation(e.g "BTC")
-This app support BTC and ETC coins only but with implementation of each coin address generation algorithm this app will support any coin
