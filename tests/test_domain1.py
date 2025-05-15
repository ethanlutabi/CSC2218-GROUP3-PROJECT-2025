# tests/test_domain.py

import pytest
from domain.accounts.checking_account import CheckingAccount
from domain.accounts.factory import AccountFactory
from domain.accounts.savings_account import SavingsAccount
from domain.accounts.service_rule import BusinessRuleService
from domain.accounts.transaction import Transaction
from uuid import UUID

def test_savings_account_deposit_withdraw():
    acc = SavingsAccount("id1", "Alice", 100.0)
    acc.deposit(50.0)
    assert acc.balance == 150.0
    acc.withdraw(20.0)
    assert acc.balance == 130.0
    with pytest.raises(ValueError):
        acc.deposit(-10.0)
    with pytest.raises(ValueError):
        acc.withdraw(200.0)

def test_account_factory_creates_correct_types():
    sav = AccountFactory.create_account("savings", "id2", "Bob", 0.0)
    chk = AccountFactory.create_account("checking", "id3", "Carol", 0.0)
    assert isinstance(sav, SavingsAccount)
    assert isinstance(chk, CheckingAccount)
    with pytest.raises(ValueError):
        AccountFactory.create_account("unknown", "id4", "Dave", 0.0)

def test_business_rule_service():
    # valid case should not raise
    BusinessRuleService.check_account_creation("Eve", 10.0, "savings")
    # invalid owner
    with pytest.raises(ValueError):
        BusinessRuleService.check_account_creation("", 10.0, "savings")
    # invalid deposit
    with pytest.raises(ValueError):
        BusinessRuleService.check_account_creation("Eve", -5.0, "checking")
    # invalid type
    with pytest.raises(ValueError):
        BusinessRuleService.check_account_creation("Eve", 0.0, "gold")

def test_transaction_fields_and_uuid():
    tx = Transaction("id1", "DEPOSIT", 30.0)
    # Check fields
    assert tx.account_id == "id1"
    assert tx.transaction_type == "DEPOSIT"
    assert tx.amount == 30.0
    # Check transaction_id is a valid UUID
    UUID(tx.transaction_id)
    # timestamp exists
    assert hasattr(tx, "timestamp")
