# Generated by Django 4.1.1 on 2022-10-07 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_cardtype_cashback_money_transaction_cashback_money'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardtype',
            name='cashback_money',
        ),
        migrations.AddField(
            model_name='card',
            name='cashback_money',
            field=models.IntegerField(blank=True, default=0, verbose_name='Сумма кэшбэка'),
        ),
    ]
