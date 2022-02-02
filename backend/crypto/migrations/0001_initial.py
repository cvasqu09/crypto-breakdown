# Generated by Django 4.0.2 on 2022-02-02 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('account_id', models.UUIDField(default=None, null=True)),
                ('name', models.CharField(max_length=128)),
                ('balance_amount', models.DecimalField(decimal_places=8, max_digits=30)),
                ('balance_currency', models.CharField(max_length=10)),
                ('native_amount', models.DecimalField(decimal_places=8, max_digits=30)),
                ('native_currency', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoTransaction',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('buy', 'Buy'), ('send', 'Send')], max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('expired', 'Expired'), ('canceled', 'Cancelled')], max_length=50)),
                ('created_at', models.DateTimeField()),
                ('amount_value', models.DecimalField(decimal_places=8, max_digits=30)),
                ('amount_currency', models.CharField(max_length=10)),
                ('native_amount_value', models.DecimalField(decimal_places=8, max_digits=30)),
                ('native_amount_currency', models.CharField(max_length=10)),
            ],
        ),
    ]