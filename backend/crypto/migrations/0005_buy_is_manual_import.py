# Generated by Django 4.0.2 on 2022-06-05 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0004_account_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='is_manual_import',
            field=models.BooleanField(default=False),
        ),
    ]
