# Generated by Django 4.1.1 on 2022-10-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0008_remove_cardtype_cashback_money_card_cashback_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_blocked',
            field=models.BooleanField(blank=True, default=False, verbose_name='заблокирована'),
        ),
        migrations.AlterField(
            model_name='card',
            name='cashback_money',
            field=models.IntegerField(blank=True, default=0, verbose_name='сумма кэшбэка'),
        ),
    ]
