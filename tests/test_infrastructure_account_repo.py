import pytest
from infrastructure.account_repo import InMemoryAccountRepository
from domain.accounts.factory import AccountFactory
from domain.interest.limits_constraint import LimitConstraint
from pytest import raises

@pytest.fixture
def repo():
    return InMemoryAccountRepository()

def test_create_and_get_account(repo):
    account = AccountFactory.create_account("checking", "acc1", "User1", 1000)
    account_id = repo.create_account(account)
    assert account_id == "acc1"
    fetched = repo.get_account("acc1")
    assert fetched.account_id == "acc1"
    assert fetched.owner == "User1"

def test_get_account_not_found(repo):
    with raises(KeyError):
        repo.get_account("nonexistent")

def test_update_account(repo):
    account = AccountFactory.create_account("checking", "acc2", "User2", 500)
    repo.create_account(account)
    account.deposit(100)
    repo.update_account(account)
    updated = repo.get_account("acc2")
    assert updated.balance == 600

def test_update_account_not_found(repo):
    account = AccountFactory.create_account("checking", "acc3", "User3", 300)
    with raises(KeyError):
        repo.update_account(account)

def test_update_accounts(repo):
    acc1 = AccountFactory.create_account("checking", "acc4", "User4", 1000)
    acc2 = AccountFactory.create_account("savings", "acc5", "User5", 2000)
    repo.create_account(acc1)
    repo.create_account(acc2)
    acc1.deposit(100)
    acc2.withdraw(500)
    repo.update_accounts(acc1, acc2)
    updated1 = repo.get_account("acc4")
    updated2 = repo.get_account("acc5")
    assert updated1.balance == 1100
    assert updated2.balance == 1500

def test_update_accounts_not_found(repo):
    acc1 = AccountFactory.create_account("checking", "acc6", "User6", 100)
    acc2 = AccountFactory.create_account("savings", "acc7", "User7", 200)
    with raises(KeyError):
        repo.update_accounts(acc1, acc2)

def test_get_and_save_constraints(repo):
    constraint = repo.get_constraints("acc8")
    assert isinstance(constraint, LimitConstraint)
    new_constraint = LimitConstraint(daily_limit=1000)
    repo.save_constraints("acc8", new_constraint)
    saved = repo.get_constraints("acc8")
    assert saved.daily_limit == 1000

def test_get_constraint_dict(repo):
    repo.save_constraints("acc9", LimitConstraint(daily_limit=500))
    constraints = repo.get_constraint_dict()
    assert "acc9" in constraints
    assert constraints["acc9"].daily_limit == 500
