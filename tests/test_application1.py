from application.services import AccountCreationService, TransactionService, AccountRepositoryInterface
from infrastructure.account_repo import InMemoryAccountRepository
from domain.accounts.factory import AccountFactory

from infrastructure.transaction_repo import InMemoryTransactionRepository
import pytest

@pytest.fixture
def account_repo():
    return InMemoryAccountRepository()

@pytest.fixture
def transaction_repo():
    return InMemoryTransactionRepository()

@pytest.fixture
def creation_service(account_repo):
    return AccountCreationService(account_repo)

@pytest.fixture
def transaction_service(account_repo, transaction_repo):
    return TransactionService(account_repo, transaction_repo)

def test_account_creation_service_success(creation_service, account_repo):
    acc_id = creation_service.create_account("savings", "test1", "Frank", 50.0)
    acc = account_repo.get_account(acc_id)
    assert acc.owner == "Frank"
    assert acc.balance == 50.0

def test_account_creation_service_invalid(creation_service):
    with pytest.raises(ValueError):
        creation_service.create_account("checking", "test2", "", 0.0)

def test_transaction_service_deposit_and_withdraw(transaction_service, account_repo):
    # create account first
    account_repo.create_account(AccountFactory.create_account("checking", "test3", "Grace", 100))
    dep_id = transaction_service.deposit("test3", 50)
    transactions = transaction_service.get_transactions("test3")
    assert len(transactions) == 1
    tx = transactions[0]
    assert tx.transaction_id == dep_id
    assert account_repo.get_account("test3").balance == 150

    # withdraw
    wit_id = transaction_service.withdraw("test3", 70)
    transactions = transaction_service.get_transactions("test3")
    assert len(transactions) == 2
    assert account_repo.get_account("test3").balance == 80

    # test invalid withdraw
    with pytest.raises(ValueError):
        transaction_service.withdraw("test3", 1000)
