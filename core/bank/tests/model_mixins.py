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


class TransactionTypeSetUpMixin(UserSetUpMixin):
    def setUp(self):
        super().setUp()
        self.transaction_type_1 = TransactionType.objects.create(
            title='Transaction type 1'
        )
        self.transaction_type_2 = TransactionType.objects.create(
            title='Transaction type 2'
        )


class CashbackSetUpMixin(TransactionTypeSetUpMixin):
    def setUp(self):
        super().setUp()

        self.cashback_1 = Cashback.objects.create(title='Cashback 1', percent=1.0)
        self.cashback_1.transaction_type.add(self.transaction_type_1)
        self.cashback_1.save()

        self.cashback_2 = Cashback.objects.create(title='Cashback 2', percent=2.0)
        self.cashback_2.transaction_type.add(self.transaction_type_2)
        self.cashback_2.save()


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


class FullSetUpMixin(TransactionSetUpMixin):
    """Предоставляет готовую mvp БД для тестирования моделей."""
    pass
