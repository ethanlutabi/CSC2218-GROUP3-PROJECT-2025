import pytest
from unittest.mock import Mock, patch
from application.services import AccountCreationService, TransactionService
from domain.accounts.factory import AccountFactory

def test_create_account_calls_repo_and_business_rule():
    mock_repo = Mock()
    service = AccountCreationService(mock_repo)

    with patch("domain.accounts.service_rule.BusinessRuleService.check_account_creation", autospec=True) as mock_check:
        account_type = "checking"
        account_id = "acc123"
        owner = "John Doe"
        initial_deposit = 1000.0

        mock_repo.create_account.return_value = account_id

        result = service.create_account(account_type, account_id, owner, initial_deposit)

        assert result == account_id
        mock_repo.create_account.assert_called_once()
        mock_check.assert_called_once_with(owner, initial_deposit, account_type)

def test_deposit_calls_repos_and_updates_account():
    mock_account_repo = Mock()
    mock_transaction_repo = Mock()
    service = TransactionService(mock_account_repo, mock_transaction_repo)

    account_id = "acc123"
    amount = 500.0

    mock_account = Mock()
    mock_account_repo.get_account.return_value = mock_account
    mock_transaction_repo.save_transaction.return_value = "tx123"

    with patch("application.services.Transaction", autospec=True) as mock_transaction_class:
        mock_transaction_class.return_value = Mock()

        result = service.deposit(account_id, amount)

        mock_account.deposit.assert_called_once_with(amount)
        mock_account_repo.update_account.assert_called_once_with(mock_account)
        mock_transaction_repo.save_transaction.assert_called_once()
        assert result == "tx123"

def test_withdraw_calls_repos_and_updates_account():
    mock_account_repo = Mock()
    mock_transaction_repo = Mock()
    service = TransactionService(mock_account_repo, mock_transaction_repo)

    account_id = "acc123"
    amount = 300.0

    mock_account = Mock()
    mock_account_repo.get_account.return_value = mock_account
    mock_transaction_repo.save_transaction.return_value = "tx456"

    with patch("application.services.Transaction", autospec=True) as mock_transaction_class:
        mock_transaction_class.return_value = Mock()

        result = service.withdraw(account_id, amount)

        mock_account.withdraw.assert_called_once_with(amount)
        mock_account_repo.update_account.assert_called_once_with(mock_account)
        mock_transaction_repo.save_transaction.assert_called_once()
        assert result == "tx456"
