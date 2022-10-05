from rest_framework.test import APITestCase

from user.serializers import AccountTarifSerializer, UserCreateUpdateSerializer
from user.models import AccountTarif, User
from bank.serializers import (
    TransactionTypeSerializer,
    CashbackCreateUpdateSerializer,
    CardTypeCreateUpdateSerializer,
    CardDesignSerializer,
    BankAccountCreateUpdateSerializer,
    CardCreateUpdateSerializer,
    DepositCreateUpdateSerializer,
    TransactionCreateUpdateSerializer
)
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


class AccountTarifSerializerTest(AccountTarifSetUpMixin, APITestCase):   
    def test_account_tarif_serializer(self):
        count = AccountTarif.objects.count()
        serializer = AccountTarifSerializer(data=self.account_tarif_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(serializer.validated_data, self.account_tarif_valid_data)
        self.assertEqual(AccountTarif.objects.count(), count + 1)

        serializer_2 = AccountTarifSerializer(data=self.account_tarif_invalid_data_1)
        self.assertEqual(serializer_2.is_valid(), False)
        self.assertListEqual(
            list(serializer_2.errors.keys()),
            ['title', 'monthly_price', 'transfer_limit', 
            'free_card_maintenance', 'additional_interest_rate']
        )


class UserSerializerTest(UserSetUpMixin, APITestCase):
    def test_user_create_serializer(self):
        count = User.objects.count()
        serializer = UserCreateUpdateSerializer(data=self.user_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(User.objects.count(), count + 1)
        self.assertEqual(serializer.instance.tarif, self.account_tarif_1)
        self.assertNotEqual(
            serializer.validated_data.pop('password'), 
            self.user_valid_data.pop('password')
        )

        serializer.validated_data.pop('tarif')
        self.user_valid_data.pop('tarif')

        self.assertEqual(serializer.validated_data, self.user_valid_data)

    def test_user_not_uniqe_serializer(self):
        serializer = UserCreateUpdateSerializer(data=self.user_valid_data)
        serializer.is_valid()
        serializer.save()

        serializer = UserCreateUpdateSerializer(data=self.user_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()),
            ['username', 'email', 'phone', 'password', 'tarif']
        )

    def test_user_phone_email_serializer(self):
        serializer = UserCreateUpdateSerializer(data=self.user_valid_data)
        serializer.is_valid()
        serializer.save()
        
        serializer = UserCreateUpdateSerializer(data=self.user_invalid_data_2)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()),
            ['username', 'email', 'phone', 'password', 'tarif']
        )


class TransactionTypeSerializerTest(TransactionTypeSetUpMixin, APITestCase):
    def test_transaction_type_serializer(self):
        count = TransactionType.objects.count()
        serializer = TransactionTypeSerializer(data=self.transaction_type_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(TransactionType.objects.count(), count + 1)

    def test_transaction_type_invalid_serializer(self):
        serializer = TransactionTypeSerializer(data=self.transaction_type_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(list(serializer.errors.keys()), ['title'])


class CashbackSerializerTest(CashbackSetUpMixin, APITestCase):
    def test_cashback_serializer(self):
        count = Cashback.objects.count()
        serializer = CashbackCreateUpdateSerializer(data=self.cashback_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(Cashback.objects.count(), count + 1)
        self.assertListEqual(
            list(serializer.instance.transaction_type.all()), 
            [self.transaction_type_1, self.transaction_type_2]
        )

    def test_cashback_invalid_1_serializer(self):
        serializer = CashbackCreateUpdateSerializer(data=self.cashback_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()), 
            ['title', 'percent', 'transaction_type']
        )

    def test_cashback_invalid_2_serializer(self):
        serializer = CashbackCreateUpdateSerializer(data=self.cashback_invalid_data_2)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()), 
            ['percent', 'transaction_type']
        )


class CardTypeSerializerTest(CardTypeSetUpMixin, APITestCase):
    def test_card_type_serializer(self):
        count = CardType.objects.count()
        serializer = CardTypeCreateUpdateSerializer(data=self.card_type_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(CardType.objects.count(), count + 1)
        self.assertListEqual(
            list(serializer.instance.cashbacks.all()), 
            [self.cashback_1, self.cashback_2]
        )

    def test_card_type_invalid_1_serializer(self):
        serializer = CardTypeCreateUpdateSerializer(data=self.card_type_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()), 
            ['title', 'push_price', 'service_price', 'cashbacks']
        )

    def test_card_type_invalid_2_serializer(self):
        serializer = CardTypeCreateUpdateSerializer(data=self.card_type_invalid_data_2)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(list(serializer.errors.keys()), ['cashbacks'])


class CardDesignSerializerTest(CardDesignSetUpMixin, APITestCase):
    def test_card_design_serializer(self):
        count = CardDesign.objects.count()
        serializer = CardDesignSerializer(data=self.card_design_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()
        self.assertEqual(CardDesign.objects.count(), count + 1)

    def test_card_desing_invalid_serializer(self):
        serializer = CardDesignSerializer(data=self.card_design_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()), 
            ['title', 'author', 'example']
        )

class BankAccountSerializerTest(BankAccountSetUpMixin, APITestCase):
    def test_bank_acoount_create_serializer(self):
        count = BankAccount.objects.count()
        serializer = BankAccountCreateUpdateSerializer(data=self.bank_account_valid_data)
        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        serializer.save()

        self.assertEqual(BankAccount.objects.count(), count + 1)
        self.assertEqual(serializer.instance.user, self.user_1)

    def test_bank_account_update_serializer(self):
        serializer = BankAccountCreateUpdateSerializer(
            instance=self.bank_account_1, 
            data=self.bank_account_update_data
        )
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(serializer.instance.user, self.user_2)
        serializer.validated_data.pop('user')
        self.bank_account_update_data.pop('user')

        self.assertEqual(serializer.validated_data, self.bank_account_update_data)

    def test_bank_account_invalid_update_serializer(self):
        serializer = BankAccountCreateUpdateSerializer(
            instance=self.bank_account_1, 
            data=self.bank_account_invalid_data_1
        )
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()), 
            ['number', 'user', 'bank_name']
        )


class CardSerializerTest(CardSetUpMixin, APITestCase):
    def test_card_create_serializer(self):
        card_count = Card.objects.count()
        bank_account_count = BankAccount.objects.count()
        serializer = CardCreateUpdateSerializer(data=self.card_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(Card.objects.count(), card_count + 1)
        self.assertEqual(BankAccount.objects.count(), bank_account_count + 1)
        self.assertEqual(serializer.instance.card_type, self.card_type_1)
        self.assertEqual(serializer.instance.design, self.card_design_1)
        self.assertEqual(serializer.validated_data['money'], self.card_valid_data['money'])

        bank_account = serializer.instance.bank_account

        self.assertEqual(bank_account.get_related_card_or_deposit(), serializer.instance)
        self.assertEqual(bank_account.number, self.card_valid_data['number'])
        self.assertEqual(bank_account.user, self.user_1)

    def test_card_create_invalid_serializer(self):
        bank_account_count = BankAccount.objects.count()
        serializer = CardCreateUpdateSerializer(data=self.card_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(BankAccount.objects.count(), bank_account_count)
        self.assertListEqual(
            list(serializer.errors.keys()),
            ['number', 'user', 'bank_name', 'currency', 'money', 'card_type', 'is_push', 'design']
        )


class DepositSerializerTest(DepositSetUpMixin, APITestCase):
    def test_deposit_create_serializer(self):
        deposit_count = Deposit.objects.count()
        bank_account_count = BankAccount.objects.count()
        serializer = DepositCreateUpdateSerializer(data=self.deposit_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(Deposit.objects.count(), deposit_count + 1)
        self.assertEqual(BankAccount.objects.count(), bank_account_count + 1)
        self.assertEqual(serializer.validated_data['money'], self.deposit_valid_data['money'])

        bank_account = serializer.instance.bank_account

        self.assertEqual(bank_account.get_related_card_or_deposit(), serializer.instance)
        self.assertEqual(bank_account.number, self.deposit_valid_data['number'])
        self.assertEqual(bank_account.user, self.user_1)

    def test_deposit_create_invalid_1_serializer(self):
        bank_account_count = BankAccount.objects.count()
        serializer = DepositCreateUpdateSerializer(data=self.deposit_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(BankAccount.objects.count(), bank_account_count)
        self.assertListEqual(
            list(serializer.errors.keys()),
            list(self.deposit_invalid_data_1.keys())
        )

    def test_deposit_create_invalid_2_serializer(self):
        bank_account_count = BankAccount.objects.count()
        serializer = DepositCreateUpdateSerializer(data=self.deposit_invalid_data_2)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(BankAccount.objects.count(), bank_account_count)
        self.assertListEqual(
            list(serializer.errors.keys()),
            list(self.deposit_invalid_data_2.keys())
        )


class TransactionSerializerTest(TransactionSetUpMixin, APITestCase):
    def test_transaction_create_serializer(self):
        count = Transaction.objects.count()
        serializer = TransactionCreateUpdateSerializer(data=self.transaction_valid_data)
        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        self.assertEqual(Transaction.objects.count(), count + 1)
        self.assertEqual(serializer.instance.from_number, self.bank_account_1)
        self.assertEqual(serializer.instance.to_number, self.bank_account_2)
        self.assertEqual(serializer.instance.transaction_type, self.transaction_type_1)

    def test_transaction_create_invalid_serializer(self):
        serializer = TransactionCreateUpdateSerializer(data=self.transaction_invalid_data_1)
        self.assertEqual(serializer.is_valid(), False)
        self.assertListEqual(
            list(serializer.errors.keys()), 
            ['from_number', 'to_number', 'money', 'currency', 'transaction_type']
        )
