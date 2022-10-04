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
from user.models import AccountTarif, User


"""
BaseSetUpMixin -> 
AccountTarifSetUpMixin -> UserSetUpMixin ->
TransactionTypeSetUpMixin -> CashbackSetUpMixin ->
CardTypeSetUpMixin -> CardDesignSetUpMixin ->
BankAccountSetUpMixin -> CardSetUpMixin ->
DepositSetUpMixin -> TransactionSetUpMixin ->
FullSetUpMixin
"""


class BaseSetUpMixin:
    def setUp(self):
        raise NotImplementedError('Need to override method setUp.')


class AccountTarifSetUpMixin(BaseSetUpMixin):
    def setUp(self):
        self.account_tarif_1 = AccountTarif.objects.create(
            title='Account tarif 1',
            monthly_price=100,
            transfer_limit=100000,
            free_card_maintenance=True,
            additional_interest_rate=1.0
        )
        self.account_tarif_2 = AccountTarif.objects.create(
            title='Account tarif 2',
            monthly_price=200,
            transfer_limit=200000,
            free_card_maintenance=True,
            additional_interest_rate=2.0
        )

        self.account_tarif_valid_data = {
            'title': 'Account tarif 11',
            'monthly_price': 100,
            'transfer_limit': 100000,
            'free_card_maintenance': False,
            'additional_interest_rate': 5.0
        }
        self.account_tarif_update_data = {
            'title': 'Account tarif 99',
            'monthly_price': 200,
            'transfer_limit': 200000,
            'free_card_maintenance': True,
            'additional_interest_rate': 10.0
        }
        self.account_tarif_invalid_data_1 = {
            'title': 'abcd'*50,  # invalid
            'monthly_price': -100,  # invalid
            'transfer_limit': -100000,  # invalid
            'free_card_maintenance': 123,  # invalid
            'additional_interest_rate': -5.0  # invalid
        }


class UserSetUpMixin(AccountTarifSetUpMixin):
    def setUp(self):
        super().setUp()
        self.user_1 = User.objects.create(
            username='User 1',
            email='user_1@gmail.com',
            phone='+79000000001',
            password='user_1_password',
            fio='User 1 FIO',
            country='User 1 country',
            tarif=self.account_tarif_1
        )
        self.user_2 = User.objects.create(
            username='User 2',
            email='user_2@gmail.com',
            phone='+79000000002',
            password='user_2_password',
            fio='User 2 FIO',
            country='User 2 country',
            tarif=self.account_tarif_2
        )

        self.user_valid_data = {
            'username': 'User 11',
            'email': 'user_11@gmail.com',
            'phone': '+79000000011',
            'password': 'user_11_password',
            'tarif': self.account_tarif_1.pk
        }
        self.user_update_data = {
            'username': 'User 99',
            'email': 'user_99@gmail.com',
            'phone': '+79000000099',
            'password': 'user_99_password',
            'tarif': self.account_tarif_2.pk
        }
        self.user_invalid_data_1 = {
            'username': 'User 11',  # invalid uniqe
            'email': 'user_11@gmail.com',  # invalid uniqe
            'phone': '+79000000011',  # invalid uniqe
            'password': '123',  # invalid
            'tarif': [self.account_tarif_1.pk, self.account_tarif_2.pk]  # invalid
        }
        self.user_invalid_data_2 = {
            'username': 'abcd'*50,  # invalid
            'email': '@gmail.com',  # invalid
            'phone': '+79000000011111111',  # invalid
            'password': 'abc',  # invalid
            'tarif': 111  # invalid
        }


class TransactionTypeSetUpMixin(UserSetUpMixin):
    def setUp(self):
        super().setUp()
        self.transaction_type_1 = TransactionType.objects.create(
            title='Transaction type 1'
        )
        self.transaction_type_2 = TransactionType.objects.create(
            title='Transaction type 2'
        )

        self.transaction_type_valid_data = {
            'title': 'Transaction type 11'
        }
        self.transaction_type_invalid_data_1 = {
            'title': 'abcd'*50  # invalid
        }


class CashbackSetUpMixin(TransactionTypeSetUpMixin):
    def setUp(self):
        super().setUp()

        self.cashback_1 = Cashback.objects.create(title='Cashback 1', percent=1.0)
        self.cashback_1.transaction_type.add(self.transaction_type_1)
        self.cashback_1.save()

        self.cashback_2 = Cashback.objects.create(title='Cashback 2', percent=2.0)
        self.cashback_2.transaction_type.add(self.transaction_type_2)
        self.cashback_2.save()

        self.cashback_valid_data = {
            'title': 'Cashback 11',
            'percent': 10,
            'transaction_type': [self.transaction_type_1.pk, self.transaction_type_2.pk]
        }
        self.cashback_invalid_data_1 = {
            'title': 'abcd'*50,  # invalid
            'percent': -10,  # invalid
            'transaction_type': self.transaction_type_1.pk  # invalid
        }
        self.cashback_invalid_data_2 = {
            'title': 123,
            'percent': 110,
            'transaction_type': [10, 20]  # invalid
        }


class CardTypeSetUpMixin(CashbackSetUpMixin):
    def setUp(self):
        super().setUp()

        self.card_type_1 = CardType.objects.create(
            title='Card type 1',
            push_price=10,
            service_price=100
        )
        self.card_type_1.cashbacks.add(self.cashback_1)
        self.card_type_1.save()

        self.card_type_2 = CardType.objects.create(
            title='Card type 2',
            push_price=20,
            service_price=200
        )
        self.card_type_2.cashbacks.add(self.cashback_2)
        self.card_type_2.save()

        self.card_type_valid_data = {
            'title': 'Card type 11',
            'push_price': 100,
            'service_price': 100,
            'cashbacks': [self.cashback_1.pk, self.cashback_2.pk]
        }
        self.card_type_invalid_data_1 = {
            'title': 'abcd'*50,  # invalid
            'push_price': -100,  # invalid
            'service_price': -100,  # invalid
            'cashbacks': self.cashback_1.pk  # invalid
        }
        self.card_type_invalid_data_2 = {
            'title': 111,
            'push_price': 100000,
            'service_price': 100000,
            'cashbacks': [10, 20]  # invalid
        }


class CardDesignSetUpMixin(CardTypeSetUpMixin):
    def setUp(self):
        super().setUp()

        self.card_design_1 = CardDesign.objects.create(
            title='Card design 1',
            author='Author 1',
            description='Description 1',
            example='Example 1'
        )
        self.card_design_2 = CardDesign.objects.create(
            title='Card design 2',
            author='Author 2',
            description='Description 2',
            example='Example 2'
        )

        self.card_design_valid_data = {
            'title': 'Card desing 11',
            'author': 'Author 1',
            'description': 'abcd'*50,
            'example': 'Example 1'
        }
        self.card_design_invalid_data_1 = {
            'title': 'abcd'*50,  # invalid
            'author': 'abcd'*50,  # invalid
            'description': 123,
            'example': 'abcd'*50  # invalid
        }


class BankAccountSetUpMixin(CardDesignSetUpMixin):
    def setUp(self):
        super().setUp()

        self.bank_account_1 = BankAccount.objects.create(
            number='00000000000000000011',
            user=self.user_1,
            bank_name='Bank 1'
        )
        self.bank_account_2 = BankAccount.objects.create(
            number='00000000000000000021',
            user=self.user_2,
            bank_name='Bank 2'
        )
        self.bank_account_3 = BankAccount.objects.create(
            number='00000000000000000012',
            user=self.user_1,
            bank_name='Bank 3'
        )
        self.bank_account_4 = BankAccount.objects.create(
            number='00000000000000000022',
            user=self.user_2,
            bank_name='Bank 4'
        )

        self.bank_account_for_update = BankAccount.objects.create(
            number='00000000000000000099',
            user=self.user_1,
            bank_name='Bank 11'
        )
        self.bank_account_valid_data = {
            'number': '00000000000000000100',
            'user': self.user_2.pk,
            'bank_name': 'Bank 22'
        }
        self.bank_account_invalid_data_1 = {
            'number': '00000000000000000011',  # invalid uniqe
            'user': [self.user_1.pk, self.user_2.pk],  # invalid
            'bank_name': 'abcd'*50  # invalid
        }


class CardSetUpMixin(BankAccountSetUpMixin):
    def setUp(self):
        super().setUp()

        self.card_1 = Card.objects.create(
            bank_account=self.bank_account_1,
            currency='RUB',
            money=10000,
            card_type=self.card_type_1,
            is_push=True,
            design=self.card_design_1
        )
        self.card_2 = Card.objects.create(
            bank_account=self.bank_account_2,
            currency='RUB',
            money=20000,
            card_type=self.card_type_2,
            is_push=True,
            design=self.card_design_2
        )

        self.card_valid_data = {
            'number': '00000000000000000999',
            'user': self.user_1.pk,
            'bank_name': 'Bank 11',
            'currency': 'RUB',
            'money': 10000.5,
            'card_type': self.card_type_1.pk,
            'is_push': False,
            'design': self.card_design_1.pk
        }
        self.card_invalid_data_1 = {
            'number': '00000000000000000011',  # invalid uniqe
            'user': [self.user_1.pk, self.user_2.pk],  # invalid
            'bank_name': 'abcd'*50,  # invalid
            'currency': 'GB',  # invalid
            'money': 'abcd',  # invalid
            'card_type': [self.card_type_1.pk, self.card_type_2.pk],  # invalid
            'is_push': 'abcd',  # invalid
            'design': [self.card_design_1.pk, self.card_design_2]  # invalid
        }


class DepositSetUpMixin(CardSetUpMixin):
    def setUp(self):
        super().setUp()

        self.deposit_1 = Deposit.objects.create(
            bank_account=self.bank_account_3,
            currency='EUR',
            money=10000,
            interest_rate=1.0,
            min_value=100,
            max_value=100000
        )
        self.deposit_2 = Deposit.objects.create(
            bank_account=self.bank_account_4,
            currency='EUR',
            money=20000,
            interest_rate=2.0,
            min_value=200,
            max_value=200000
        )

        self.deposit_valid_data = {
            'number': '00000000000000000888',
            'user': self.user_1.pk,
            'bank_name': 'Bank 11',
            'currency': 'RUB',
            'money': 10000.5,
            'min_value': 1000,
            'max_value': 100000
        }
        self.deposit_invalid_data_1 = {
            'number': '00000000000000000011',  # invalid uniqe
            'user': [self.user_1.pk, self.user_2.pk],  # invalid
            'bank_name': 'abcd'*50,  # invalid
            'currency': 'GB',  # invalid
            'money': 'abcd',  # invalid
            'min_value': -1000,  # invalid
            'max_value': -100000  # invalid
        }
        self.deposit_invalid_data_2 = {
            'number': '0000000111',  # invalid
            'user': 20,  # invalid
            'bank_name': 'abcd'*50,  # invalid
            'currency': 'GB',  # invalid
            'money': 'abcd',  # invalid
            'min_value': 'abcd',  # invalid
            'max_value': 'abcd'  # invalid
        }


class TransactionSetUpMixin(DepositSetUpMixin):
    def setUp(self):
        super().setUp()

        self.transaction_1 = Transaction.objects.create(
            from_number=self.bank_account_1,
            to_number=self.bank_account_2,
            money=1000,
            currency='RUB',
            transaction_type=self.transaction_type_1
        )
        self.transaction_2 = Transaction.objects.create(
            from_number=self.bank_account_3,
            to_number=self.bank_account_4,
            money=2000,
            currency='EUR',
            transaction_type=self.transaction_type_2
        )

        self.transaction_valid_data = {
            'from_number': self.bank_account_1.pk,
            'to_number': self.bank_account_2.pk,
            'money': 1000,
            'currency': 'RUB',
            'transaction_type': self.transaction_type_1.pk
        }
        self.transaction_invalid_data_1 = {
            'from_number': [self.bank_account_1.pk, self.bank_account_3],  # invalid
            'to_number': [self.bank_account_2.pk, self.bank_account_4],  # invalid
            'money': -1000,  # invalid
            'currency': 'GB',  # invalid
            'transaction_type': [self.transaction_type_1.pk, self.transaction_type_2.pk]  # invalid
        }


class FullSetUpMixin(TransactionSetUpMixin):
    """Предоставляет готовую mvp БД для тестирования моделей."""
    pass
