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
        self.assertEqual(response.data.pop('tarif')['id'], self.user_valid_data.pop('tarif'))
        self.assertDictEqual(response.data, self.user_valid_data)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_user_retrive_update_delete(self):
        self.client.post(self.url, self.user_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_valid_data['username'])
        self.assertEqual(response.data.pop('tarif')['id'], self.user_valid_data.pop('tarif'))

        response = self.client.put(self.url_detail, self.user_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response.data.pop('id')
        self.user_update_data.pop('password')
        self.assertEqual(response.data.pop('tarif')['id'], self.user_update_data.pop('tarif'))
        self.assertEqual(response.data, self.user_update_data)

        count = User.objects.count()
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), count - 1)

    def test_user_invalid_api(self):
        response = self.client.post(self.url, self.user_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.user_invalid_data_1.keys())
        )


class TransactionTypeAPITest(TransactionTypeSetUpMixin, APITestCase):
    url = reverse('transaction_type')
    url_detail = reverse('transaction_type_detail', kwargs={'pk': 3})
    
    def test_transaction_type_list_create_api(self):
        count = TransactionType.objects.count()
        response = self.client.post(self.url, self.transaction_type_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response.data.pop('id')
        self.assertEqual(response.data, self.transaction_type_valid_data)
        self.assertEqual(TransactionType.objects.count(), count + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_transaction_type_retrive_update_delete_api(self):
        self.client.post(self.url, data=self.transaction_type_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.transaction_type_valid_data['title'])

        response = self.client.put(self.url_detail, self.transaction_type_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.transaction_type_update_data['title'])

        count = TransactionType.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TransactionType.objects.count(), count - 1)

    def test_transaction_type_invalid_api(self):
        response = self.client.post(self.url, self.transaction_type_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.transaction_type_invalid_data_1.keys())
        )


class CashbackAPITest(CashbackSetUpMixin, APITestCase):
    url = reverse('cashback')
    url_detail = reverse('cashback_detail', kwargs={'pk': 3})
    
    def test_cashback_list_create_api(self):
        count = Cashback.objects.count()
        response = self.client.post(self.url, self.cashback_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response.data.pop('id')
        self.assertListEqual(
            list(tr_typ['id'] for tr_typ in response.data.pop('transaction_type')),
            self.cashback_valid_data.pop('transaction_type')
        )
        self.assertEqual(response.data, self.cashback_valid_data)
        self.assertEqual(Cashback.objects.count(), count + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_cashback_retrive_update_delete_api(self):
        self.client.post(self.url, data=self.cashback_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.cashback_valid_data['title'])

        response = self.client.put(self.url_detail, self.cashback_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response.data.pop('id')
        self.assertListEqual(
            list(tr_typ['id'] for tr_typ in response.data.pop('transaction_type')),
            self.cashback_update_data.pop('transaction_type')
        )
        self.assertEqual(response.data, self.cashback_update_data)

        count = Cashback.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cashback.objects.count(), count - 1)

    def test_cashback_invalid_api(self):
        response = self.client.post(self.url, self.cashback_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.cashback_invalid_data_1.keys())
        )


class CardTypeAPITest(CardTypeSetUpMixin, APITestCase):
    url = reverse('card_type')
    url_detail = reverse('card_type_detail', kwargs={'pk': 3})
    
    def test_card_type_list_create_api(self):
        count = CardType.objects.count()
        response = self.client.post(self.url, self.card_type_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response.data.pop('id')
        self.assertListEqual(
            list(cas['id'] for cas in response.data.pop('cashbacks')),
            self.card_type_valid_data.pop('cashbacks')
        )
        self.assertEqual(response.data, self.card_type_valid_data)
        self.assertEqual(CardType.objects.count(), count + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_card_type_retrive_update_delete_api(self):
        self.client.post(self.url, data=self.card_type_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.card_type_valid_data['title'])

        response = self.client.put(self.url_detail, self.card_type_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response.data.pop('id')
        self.assertListEqual(
            list(cas['id'] for cas in response.data.pop('cashbacks')),
            self.card_type_update_data.pop('cashbacks')
        )
        self.assertEqual(response.data, self.card_type_update_data)

        count = CardType.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CardType.objects.count(), count - 1)

    def test_card_type_invalid_api(self):
        response = self.client.post(self.url, self.card_type_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.card_type_invalid_data_1.keys())
        )


class CardDesignAPITest(CardDesignSetUpMixin, APITestCase):
    url = reverse('card_design')
    url_detail = reverse('card_design_detail', kwargs={'pk': 3})
    
    def test_card_design_list_create_api(self):
        count = CardDesign.objects.count()
        response = self.client.post(self.url, self.card_design_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response.data.pop('id')
        self.assertEqual(response.data, self.card_design_valid_data)
        self.assertEqual(CardDesign.objects.count(), count + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_card_design_retrive_update_delete_api(self):
        self.client.post(self.url, data=self.card_design_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.card_design_valid_data['title'])

        response = self.client.put(self.url_detail, self.card_design_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response.data.pop('id')
        self.assertEqual(response.data, self.card_design_update_data)

        count = CardDesign.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CardDesign.objects.count(), count - 1)

    def test_card_design_invalid_api(self):
        response = self.client.post(self.url, self.card_design_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.card_design_invalid_data_1.pop('description')
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.card_design_invalid_data_1.keys())
        )


class BankAccountAPITest(BankAccountSetUpMixin, APITestCase):
    url = reverse('bank_account')
    url_detail = reverse('bank_account_detail', kwargs={'pk': 1})

    def setUp(self):
        super().setUp()
        self.deposit_for_delete = Deposit.objects.create(
            bank_account=self.bank_account_1,
            currency='EUR',
            money=20000,
            interest_rate=2.0,
            min_value=200,
            max_value=200000
        )
    
    def test_bank_account_list_create_api(self):
        count = BankAccount.objects.count()
        response = self.client.post(self.url, self.bank_account_valid_data)  # post not allowed.
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(BankAccount.objects.count(), count)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)

    def test_bank_account_retrive_update_api(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['number'], self.bank_account_1.number)
        self.assertEqual(response.data['user']['id'], self.bank_account_1.user.pk)

        response = self.client.put(self.url_detail, self.bank_account_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response.data.pop('id')
        self.assertEqual(response.data.pop('user')['id'], self.bank_account_update_data.pop('user'))
        self.assertEqual(response.data, self.bank_account_update_data)

    def test_bank_account_delete_api(self):
        bank_account_count = BankAccount.objects.count()
        deposit_count = Deposit.objects.count()

        related_obj = self.bank_account_1.get_related_card_or_deposit()
        self.assertEqual(related_obj, self.deposit_for_delete)

        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(BankAccount.objects.count(), bank_account_count - 1)
        self.assertEqual(Deposit.objects.count(), deposit_count - 1)

    def test_bank_account_update_invalid_api(self):
        response = self.client.put(self.url_detail, self.bank_account_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.bank_account_invalid_data_1.keys())
        )


class CardAPITest(CardSetUpMixin, APITestCase):
    url = reverse('card')
    url_detail = reverse('card_detail', kwargs={'pk': 3})
    
    def test_card_list_create_api(self):
        card_count = Card.objects.count()
        bank_account_count = BankAccount.objects.count()

        response = self.client.post(self.url, self.card_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.data['bank_account']['id'], 
            BankAccount.objects.get(pk=bank_account_count + 1).pk
        )
        self.assertEqual(
            response.data.pop('bank_account')['user'], 
            self.card_valid_data['user']
        )
        self.assertEqual(response.data.pop('card_type')['id'], self.card_valid_data.pop('card_type'))
        self.assertEqual(response.data.pop('design')['id'], self.card_valid_data.pop('design'))

        self.assertEqual(Card.objects.count(), card_count + 1)
        self.assertEqual(BankAccount.objects.count(), bank_account_count + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), card_count + 1)

    def test_card_retrive_update_api(self):
        self.client.post(self.url, self.card_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['bank_account']['number'], 
            self.card_valid_data['number']
        )

        response = self.client.put(self.url_detail, self.card_update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bank_account']['user'], self.card_update_data['user'])
        self.assertEqual(response.data['bank_account']['number'], self.card_update_data['number'])
        self.assertEqual(response.data['card_type']['id'], self.card_update_data['card_type'])
        self.assertEqual(response.data['design']['id'], self.card_update_data['design'])

    def test_card_delete_api(self):
        self.client.post(self.url, self.card_valid_data)

        card_count = Card.objects.count()
        bank_acoount_count = BankAccount.objects.count()

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Card.objects.count(), card_count - 1)
        self.assertEqual(BankAccount.objects.count(), bank_acoount_count - 1)

    def test_card_invalid_api(self):
        response = self.client.post(self.url, self.card_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.card_invalid_data_1.keys())
        )


class DepositAPITest(DepositSetUpMixin, APITestCase):
    url = reverse('deposit')
    url_detail = reverse('deposit_detail', kwargs={'pk': 3})
    
    def test_deposit_list_create_api(self):
        deposit_count = Deposit.objects.count()
        bank_account_count = BankAccount.objects.count()

        response = self.client.post(self.url, self.deposit_valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['bank_account']['id'], 
            BankAccount.objects.get(pk=bank_account_count + 1).pk
        )
        self.assertEqual(
            response.data['bank_account']['number'], 
            self.deposit_valid_data.pop('number')
        )
        self.assertEqual(
            response.data.pop('bank_account')['user'], 
            self.deposit_valid_data.pop('user')
        )

        self.assertEqual(Deposit.objects.count(), deposit_count + 1)
        self.assertEqual(BankAccount.objects.count(), bank_account_count + 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), deposit_count + 1)

    def test_deposit_retrive_update_api(self):
        self.client.post(self.url, self.deposit_valid_data)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['bank_account']['number'], 
            self.deposit_valid_data['number']
        )

        response = self.client.put(self.url_detail, self.deposit_update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bank_account']['user'], self.deposit_update_data['user'])
        self.assertEqual(response.data['bank_account']['number'], self.deposit_update_data['number'])

    def test_deposit_delete_api(self):
        self.client.post(self.url, self.deposit_valid_data)

        deposit_count = Deposit.objects.count()
        bank_acoount_count = BankAccount.objects.count()

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Deposit.objects.count(), deposit_count - 1)
        self.assertEqual(BankAccount.objects.count(), bank_acoount_count - 1)

    def test_deposit_invalid_api(self):
        response = self.client.post(self.url, self.deposit_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.deposit_invalid_data_1.keys())
        )


class TransactionAPITest(TransactionSetUpMixin, APITestCase):
    url = reverse('transaction')
    url_detail = reverse('transaction_detail', kwargs={'pk': 3})
    
    def test_transaction_list_create_api(self):
        count = Transaction.objects.count()
        response = self.client.post(self.url, self.transaction_valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), count + 1)
        self.assertEqual(
            response.data['from_number']['id'], 
            self.transaction_valid_data['from_number']
        )
        self.assertEqual(
            response.data['to_number']['id'], 
            self.transaction_valid_data['to_number']
        )
        self.assertEqual(
            response.data['transaction_type']['id'], 
            self.transaction_valid_data['transaction_type']
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)

    def test_transaction_retrive_update_api(self):
        self.client.post(self.url, self.transaction_valid_data)
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['from_number']['id'], 
            self.transaction_valid_data['from_number']
        )
        self.assertEqual(
            response.data['to_number']['id'], 
            self.transaction_valid_data['to_number']
        )
        self.assertEqual(
            response.data['transaction_type']['id'], 
            self.transaction_valid_data['transaction_type']
        )

        response = self.client.put(self.url_detail, self.transaction_update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['from_number']['id'], 
            self.transaction_update_data['from_number']
        )
        self.assertEqual(
            response.data['to_number']['id'], 
            self.transaction_update_data['to_number']
        )
        self.assertEqual(
            response.data['transaction_type']['id'], 
            self.transaction_update_data['transaction_type']
        )

    def test_transaction_delete_api(self):
        self.client.post(self.url, self.transaction_valid_data)
        count = Transaction.objects.count()

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), count - 1)

    def test_transaction_invalid_api(self):
        response = self.client.post(self.url, self.transaction_invalid_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response.data.keys()), 
            list(self.transaction_invalid_data_1.keys())
        )
