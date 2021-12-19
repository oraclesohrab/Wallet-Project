from django.db import models
from django.conf import settings


class Currency(models.Model):
    name = models.CharField(max_length=20)
    abbr = models.CharField(max_length=10)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'wallet'
        db_table = 'currency'
        verbose_name = ('currency')
        verbose_name_plural = ('currencies')

    def __str__(self):
        return '{}({})'.format(self.name, self.abbr)


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_user")
    currency = models.ForeignKey(to='Currency', on_delete=models.CASCADE, related_name="wallet_coin")
    address = models.CharField(max_length=50)
    ballance = models.DecimalField(decimal_places=10, max_digits=50, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    public_key = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'currency')
        app_label = 'wallet'
        db_table = 'wallet'
        verbose_name = ('wallet')
        verbose_name_plural = ('wallets')
    
    def __str__(self):
        return '{}({})'.format(self.user.username, self.currency.abbr)