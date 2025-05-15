import pytest
from domain.accounts.checking_account import CheckingAccount
from domain.accounts.savings_account import SavingsAccount
from domain.accounts.factory import AccountFactory
from application.transfer_logging.notifications_services import NotificationService
from application.transfer_logging.transfer_service import FundTransferService
from infrastructure.adapters.logging import TransactionServiceLogger
from infrastructure.account_repo import InMemoryAccountRepository
from infrastructure.transaction_repo import InMemoryTransactionRepository
from infrastructure.adapters.notify import ConsoleNotificationAdapter
from infrastructure.adapters.logging import ConsoleLogger


@pytest.fixture
def account_repo():
    repo = InMemoryAccountRepository()
    # Pre-populate two accounts for transfers
    repo.create_account(AccountFactory.create_account("checking", "SRC", "Alice", 100.0))
    repo.create_account(AccountFactory.create_account("savings",  "DST", "Bob",   50.0))
    return repo

@pytest.fixture
def transaction_repo():
    return InMemoryTransactionRepository()

@pytest.fixture
def notifier(capsys):
    # We'll capture print output via capsys
    return ConsoleNotificationAdapter()

@pytest.fixture
def logger(capsys):
    return ConsoleLogger()

@pytest.fixture
def fund_service(account_repo, transaction_repo, notifier):
    return FundTransferService(account_repo, transaction_repo, notification_adapter=notifier)

@pytest.fixture
def tx_service(account_repo, transaction_repo, logger):
    from application.services import TransactionService
    base = TransactionService(account_repo, transaction_repo)
    return TransactionServiceLogger(base, logger)

def test_fund_transfer_success_and_notification(capsys, fund_service, account_repo, transaction_repo):
    tx_id = fund_service.transfer_funds("SRC", "DST", 30.0)
    # Balances updated
    assert account_repo.get_account("SRC").balance == 70.0
    assert account_repo.get_account("DST").balance == 80.0
    # Transaction saved
    tx = transaction_repo.find_transaction_by_id(tx_id)
    assert tx.transaction_type == "TRANSFER"
    # Notification printed
    captured = capsys.readouterr()
    assert "[EMAIL]" in captured.out
    assert "Transferred 30.0 from SRC to DST" in captured.out

def test_fund_transfer_insufficient_funds_raises(fund_service):
    with pytest.raises(ValueError):
        fund_service.transfer_funds("SRC", "DST", 200.0)

def test_transaction_service_logger_deposit_and_withdraw(capsys, tx_service, account_repo):
    # Deposit
    tx_id1 = tx_service.deposit("SRC", 20.0)
    assert account_repo.get_account("SRC").balance == 120.0
    out1 = capsys.readouterr().out
    assert "[LOG] Deposit of 20.0 to SRC, tx_id=" in out1

    # Withdraw
    tx_id2 = tx_service.withdraw("SRC", 50.0)
    assert account_repo.get_account("SRC").balance == 70.0
    out2 = capsys.readouterr().out
    assert "[LOG] Withdraw of 50.0 from SRC, tx_id=" in out2

def test_transaction_service_list_and_get_transaction(capsys, tx_service, account_repo, transaction_repo):
    # Make a deposit so there’s a tx to list
    tx_id = tx_service.deposit("SRC", 10.0)
    # List all
    txs = tx_service.get_transactions("SRC")
    assert any(t.transaction_id == tx_id for t in txs)
    # Get single via service method (must exist)
    # We need to expose get_transaction on the decorator
    single = tx_service.get_transaction(tx_id)
    assert single.transaction_id == tx_id
    out = capsys.readouterr().out
    # since logger logs get_transaction, it should appear
    assert f"Fetching transaction {tx_id}" in out
