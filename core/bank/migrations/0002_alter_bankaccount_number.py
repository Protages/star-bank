# Generated by Django 4.1.1 on 2022-09-23 16:38

import bank.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='number',
            field=models.CharField(max_length=20, unique=True, validators=[bank.validators.number_validation], verbose_name='номер счета'),
        ),
    ]
