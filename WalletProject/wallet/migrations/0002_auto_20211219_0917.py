# Generated by Django 2.2.2 on 2021-12-19 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='abbv',
            new_name='abbr',
        ),
    ]
