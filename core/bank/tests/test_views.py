from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from user.models import AccountTarif, User
from bank.models import (
    BankAccount,
    TransactionType,
    Transaction,
    Cashback,
    CardType,
    CardDesign,
    Card,
    Deposit,
)
from .model_mixins import *


class AccountTarifAPITest(AccountTarifSetUpMixin, APITestCase):
    url = reverse('account_tarif')
    url_detail = reverse('account_tarif_detail', kwargs={'pk': 3})

    def test_account_tarif_list_create_api(self):
        count = AccountTarif.objects.count()
        response = self.client.post(self.url, self.account_tarif_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response.data.pop('id')

        self.assertEqual(AccountTarif.objects.count(), count + 1)
        self.assertDictEqual(response.data, self.account_tarif_valid_data)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_account_tarif_retrive_update_delete_api(self):
        self.client.post(self.url, self.account_tarif_valid_data)
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.account_tarif_valid_data['title'])

        response = self.client.put(self.url_detail, self.account_tarif_update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.data.pop('id')
        self.assertEqual(response.data, self.account_tarif_update_data)

        count = AccountTarif.objects.count()
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AccountTarif.objects.count(), count - 1)

    def test_account_tarif_invalid_api(self):
        response = self.client.post(self.url, self.account_tarif_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAPITest(UserSetUpMixin, APITestCase):
    url = reverse('user')
    url_detail = reverse('user_detail', kwargs={'pk': 3})

    def test_user_list_create_api(self):
        count = User.objects.count()
        response = self.client.post(self.url, self.user_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response.data.pop('id')
        self.user_valid_data.pop('password')

        self.assertEqual(User.objects.count(), count + 1)
        self.assertDictEqual(response.data, self.user_valid_data)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_user_retrive_update_delete(self):
        self.client.post(self.url, self.user_valid_data)
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_valid_data['username'])

        response = self.client.put(self.url_detail, self.user_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response.data.pop('id')
        self.user_update_data.pop('password')
        self.assertEqual(response.data, self.user_update_data)

        count = User.objects.count()
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), count - 1)
