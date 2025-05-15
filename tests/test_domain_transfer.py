import pytest
from domain.accounts.checking_account import CheckingAccount
from domain.accounts.savings_account import SavingsAccount
from domain.transfer.transfer import TransferTransaction
from domain.transfer.transfer_service import TransferService


def test_transfer_transaction_inherits_transaction_fields():
    tx = TransferTransaction("A1", "A2", 25.0)
    # It should have a valid UUID and timestamp
    assert hasattr(tx, "transaction_id")
    assert hasattr(tx, "timestamp")
    assert tx.source_account_id == "A1"
    assert tx.dest_account_id == "A2"
    assert tx.amount == 25.0
    assert tx.transaction_type == "TRANSFER"

def test_successful_transfer_updates_balances():
    a_src = CheckingAccount("A1", "Alice", balance=100.0)
    a_dest = SavingsAccount("A2", "Bob", balance=50.0)

    tx = TransferService.execute(a_src, a_dest, 40.0)
    # Balances should reflect the move
    assert a_src.balance == 60.0
    assert a_dest.balance == 90.0
    # Transaction object should reference correct accounts and amount
    assert isinstance(tx, TransferTransaction)
    assert tx.source_account_id == "A1"
    assert tx.dest_account_id == "A2"
    assert tx.amount == 40.0

def test_transfer_insufficient_funds_raises():
    a_src = SavingsAccount("A1", "Alice", balance=10.0)
    a_dest = CheckingAccount("A2", "Bob", balance=0.0)
    with pytest.raises(ValueError):
        TransferService.execute(a_src, a_dest, 20.0)
