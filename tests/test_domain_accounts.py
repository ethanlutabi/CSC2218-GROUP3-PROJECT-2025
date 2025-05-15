from domain.accounts import factory, transaction

def test_create_checking_account():
    account = factory.AccountFactory.create_account("checking", "123", "John Doe", 1000)
    assert account.account_id == "123"
    assert account.owner == "John Doe"
    assert account.balance == 1000
    assert account.account_type() == "checking"

def test_create_savings_account():
    account = factory.AccountFactory.create_account("savings", "456", "Jane Doe", 2000)
    assert account.account_id == "456"
    assert account.owner == "Jane Doe"
    assert account.balance == 2000
    assert account.account_type() == "savings"

def test_deposit_transaction():
    account = factory.AccountFactory.create_account("checking", "789", "Alice", 500)
    txn = transaction.Transaction("txn1", "DEPOSIT", 200)
    account.deposit(txn.amount)
    assert account.balance == 700

def test_withdraw_transaction():
    account = factory.AccountFactory.create_account("checking", "101", "Bob", 500)
    txn = transaction.Transaction("txn2", "WITHDRAW", 300)
    account.withdraw(txn.amount)
    assert account.balance == 200
