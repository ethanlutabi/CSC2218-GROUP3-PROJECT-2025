import sys
import os
from datetime import datetime
from unittest.mock import MagicMock
from unittest import TestCase

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.fund_transfer_services import FundTransferService
from domain.account import Account, AccountType, AccountStatus
from domain.transaction import TransactionType

class TestFundTransferService(TestCase):
    def setUp(self):
        self.mock_account_repo = MagicMock()
        self.mock_transaction_repo = MagicMock()
        self.service = FundTransferService(self.mock_account_repo, self.mock_transaction_repo)
        
        # Create test accounts with all required parameters
        self.source = Account(
            account_id="acc1",
            account_type=AccountType.CHECKING,
            balance=100.0,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
        self.dest = Account(
            account_id="acc2",
            account_type=AccountType.SAVINGS,
            balance=50.0,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
        
        # Configure mock to return our test accounts
        self.mock_account_repo.find_by_id.side_effect = lambda x: (
            self.source if x == "acc1" else (self.dest if x == "acc2" else None)
        )

    def test_successful_transfer(self):
        """Test that funds are transferred correctly between accounts"""
        # Perform transfer
        transaction = self.service.transfer_funds("acc1", "acc2", 30.0)
        
        # Verify balances were updated
        self.assertEqual(self.source.balance, 70.0)
        self.assertEqual(self.dest.balance, 80.0)
        
        # Verify transaction record was created
        self.assertEqual(transaction.transaction_type, TransactionType.TRANSFER)
        self.assertEqual(transaction.amount, 30.0)
        self.assertEqual(transaction.account_id, "acc1")
        self.assertEqual(transaction.destination_account_id, "acc2")
        
        # Verify repositories were called
        self.mock_account_repo.find_by_id.assert_any_call("acc1")
        self.mock_account_repo.find_by_id.assert_any_call("acc2")
        self.mock_account_repo.save.assert_any_call(self.source)
        self.mock_account_repo.save.assert_any_call(self.dest)
        self.mock_transaction_repo.save.assert_called_once()

    def test_transfer_to_same_account(self):
        """Test that transferring to the same account fails"""
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc1", 30.0)

    def test_insufficient_funds(self):
        """Test that transfer fails with insufficient funds"""
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc2", 150.0)

    def test_inactive_source_account(self):
        """Test that transfer fails if source account is inactive"""
        self.source.status = AccountStatus.CLOSED
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc2", 30.0)

    def test_inactive_destination_account(self):
        """Test that transfer fails if destination account is inactive"""
        self.dest.status = AccountStatus.CLOSED
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc2", 30.0)