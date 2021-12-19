from django.urls import path
from .views import *

urlpatterns = [
    path('create_wallet/', create_wallet_view, name='create_wallet'),
    path('user_wallet_list/', wallet_list_view, name='user_wallets'),
    path('get_wallet/', get_wallet_view, name='get_wallet'),
    path('all_wallets_list/', all_wallet_list_view, name='all_wallets'),
    path('admin_get_wallet/', get_wallet_admin_view, name='admin_get_wallet'),
    path('get_backup/', get_backup_view, name='get_backup'),
]
