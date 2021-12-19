# Generated by Django 2.2.2 on 2021-12-18 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('abbv', models.CharField(max_length=10)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
                'db_table': 'currency',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50)),
                ('ballance', models.DecimalField(decimal_places=10, max_digits=50)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('private_key', models.BinaryField()),
                ('public_key', models.CharField(max_length=100)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_coin', to='wallet.Currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'wallet',
                'verbose_name_plural': 'wallets',
                'db_table': 'wallet',
                'unique_together': {('user', 'currency')},
            },
        ),
    ]
