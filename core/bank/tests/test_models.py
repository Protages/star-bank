from django.test import TestCase
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
from .model_mixins import (
    AccountTarifSetUpMixin,
    UserSetUpMixin,
    TransactionTypeSetUpMixin,
    CashbackSetUpMixin,
    CardTypeSetUpMixin,
    CardDesignSetUpMixin,
    BankAccountSetUpMixin,
    CardSetUpMixin,
    DepositSetUpMixin,
    TransactionSetUpMixin,
)


class AccountTarifTest(AccountTarifSetUpMixin, TestCase):
    def test_account_tarif_title(self):
        account_tarif_1 = AccountTarif.objects.get(pk=1)
        account_tarif_2 = AccountTarif.objects.get(pk=2)
        self.assertEqual(account_tarif_1.title, 'Account tarif 1')
        self.assertEqual(account_tarif_1.transfer_limit, 100000)
        self.assertEqual(account_tarif_2.title, 'Account tarif 2')
        self.assertEqual(account_tarif_2.transfer_limit, 200000)


class UserTest(UserSetUpMixin, TestCase):
    def test_user_username(self):
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        self.assertEqual(user_1.username, 'User 1')
        self.assertEqual(user_1.tarif, self.account_tarif_1)
        self.assertEqual(user_2.username, 'User 2')
        self.assertEqual(user_2.tarif, self.account_tarif_2)


class TransactionTypeTest(TransactionTypeSetUpMixin, TestCase):
    def test_transaction_type_title(self):
        transaction_type_1 = TransactionType.objects.get(pk=1)
        transaction_type_2 = TransactionType.objects.get(pk=2)
        self.assertEqual(transaction_type_1.title, 'Transaction type 1')
        self.assertEqual(transaction_type_2.title, 'Transaction type 2')


class CashbackTest(CashbackSetUpMixin, TestCase):
    def test_cashback(self):
        cashback_1 = Cashback.objects.get(pk=1)
        cashback_2 = Cashback.objects.get(pk=2)
        self.assertEqual(cashback_1.title, 'Cashback 1')
        self.assertEqual(cashback_1.transaction_type.all()[0], self.transaction_type_1)
        self.assertEqual(cashback_2.title, 'Cashback 2')
        self.assertEqual(cashback_2.transaction_type.all()[0], self.transaction_type_2)


class CardTypeTest(CardTypeSetUpMixin, TestCase):
    def test_card_type(self):
        card_type_1 = CardType.objects.get(pk=1)
        card_type_2 = CardType.objects.get(pk=2)
        self.assertEqual(card_type_1.title, 'Card type 1')
        self.assertEqual(card_type_1.cashbacks.all()[0], self.cashback_1)
        self.assertEqual(card_type_2.title, 'Card type 2')
        self.assertEqual(card_type_2.cashbacks.all()[0], self.cashback_2)


class CardDesignTest(CardDesignSetUpMixin, TestCase):
    def test_card_design(self):
        card_design_1 = CardDesign.objects.get(pk=1)
        card_design_2 = CardDesign.objects.get(pk=2)
        self.assertEqual(card_design_1.title, 'Card design 1')
        self.assertEqual(card_design_2.title, 'Card design 2')


class BankAccountTest(BankAccountSetUpMixin, TestCase):
    def test_bank_account(self):
        bank_account_1 = BankAccount.objects.get(pk=1)
        bank_account_2 = BankAccount.objects.get(pk=2)
        self.assertEqual(bank_account_1.number, '00000000000000000011')
        self.assertEqual(bank_account_1.user, self.user_1)
        self.assertEqual(bank_account_2.number, '00000000000000000021')
        self.assertEqual(bank_account_2.user, self.user_2)


class CardTest(CardSetUpMixin, TestCase):
    def test_card(self):
        card_1 = Card.objects.get(pk=1)
        card_2 = Card.objects.get(pk=2)

        self.assertEqual(card_1.bank_account, self.bank_account_1)
        self.assertEqual(card_1.card_type, self.card_type_1)
        self.assertEqual(card_1.design, self.card_design_1)

        self.assertEqual(card_2.bank_account, self.bank_account_2)
        self.assertEqual(card_2.card_type, self.card_type_2)
        self.assertEqual(card_2.design, self.card_design_2)


class DepositTest(DepositSetUpMixin, TestCase):
    def test_deposit(self):
        deposit_1 = Deposit.objects.get(pk=1)
        deposit_2 = Deposit.objects.get(pk=2)

        self.assertEqual(deposit_1.bank_account, self.bank_account_3)
        self.assertEqual(deposit_1.min_value, 100)

        self.assertEqual(deposit_2.bank_account, self.bank_account_4)
        self.assertEqual(deposit_2.min_value, 200)


class TransactionTest(TransactionSetUpMixin, TestCase):
    def test_transaction(self):
        transaction_1 = Transaction.objects.get(pk=1)
        transaction_2 = Transaction.objects.get(pk=2)

        self.assertEqual(transaction_1.from_number, self.bank_account_1)
        self.assertEqual(transaction_1.to_number, self.bank_account_2)
        self.assertEqual(transaction_1.transaction_type, self.transaction_type_1)

        self.assertEqual(transaction_2.from_number, self.bank_account_3)
        self.assertEqual(transaction_2.to_number, self.bank_account_4)
        self.assertEqual(transaction_2.transaction_type, self.transaction_type_2)
