Порядок действий для создания MVP бд.

1. (обязательно) Создание записи AccountTarif
    "http://127.0.0.1:8000/api/v1/account_tarif/"

2. (обязательно) Создание записи User, и привязка AccountTarif (число, int)
    "http://127.0.0.1:8000/api/v1/user/"

3. (обязательно) Создание записи TransactionType
    "http://127.0.0.1:8000/api/v1/transaction_type/"

4. (обязательно) Создание записи Cashback, и привязка TransactionType (список, int)
    "http://127.0.0.1:8000/api/v1/cashback/"

5. (обязательно) Создание записи CardType, и привязка Cashback (список, int)
    "http://127.0.0.1:8000/api/v1/card_type/"

6. (не обязательно) Создание записи CardDesign
    "http://127.0.0.1:8000/api/v1/card_design/"

7. (обязательно) Создание записи Card (или Deposit) и привязка CardType и CardDesign (число, int).
    При этом будет создана запись BankAccount, поэтому необходимо также передать соотв. данные.
    "http://127.0.0.1:8000/api/v1/card/"
    "http://127.0.0.1:8000/api/v1/deposit/" 


Создание и обновление записи Card или Deposit.
При создании и обновлении записи Card или Deposit будет создаваться и обновляться связанная запись BankAccount.
При удалении записи Card или Deposit будет удаляться связанная запись BankAccount.
Поля number, user, bank_name относятся к таблице BankAccount, по ним будет создана запись.

Card:
{
    "number": "",
    "user": 0,
    "bank_name": "",
    "currency": "RUB",
    "money": 1000.0,
    "card_type": 0,
    "is_push": false,
    "design": 0
}

Deposit:
{
    "number": "",
    "user": 0,
    "bank_name": "",
    "currency": "RUB",
    "money": 1000.0,
    "interest_rate": 0.0,
    "min_value": 0,
    "max_value": 100000
}


Про BankAccount.

1. Напрмую создать запись BankAccount нельзя. 
2. Для создания необходимо создать запись Card или Deposit, передав при этом данные для BankAccount.
3. Можно обновить запись BankAccount.
4. При удалении записи BankAccount, будет удалена связанная запись Card или Deposit(!)
