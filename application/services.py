from abc import ABC, abstractmethod
from typing import List
from domain.accounts.create_accounts import Account, AccountFactory
from domain.accounts.transaction import Transaction
from domain.accounts.services import BusinessRuleService


# Repository interfaces for Application Layer
class AccountRepositoryInterface(ABC):
    @abstractmethod
    def create_account(self, account: Account) -> str:
        """Persist a new account and return its ID."""
        pass

    @abstractmethod
    def get_account(self, account_id: str) -> Account:
        """Retrieve an account by its ID."""
        pass

    @abstractmethod
    def update_account(self, account: Account) -> None:
        """Update an existing account's state."""
        pass

    @abstractmethod
    def update_accounts(self, source: Account, dest: Account) -> None:
        """Atomically update two accounts (for transfers)."""
        pass

class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def save_transaction(self, transaction: Transaction) -> str:
        """Persist a new transaction and return its ID."""
        pass

    @abstractmethod
    def list_transactions(self, account_id: str) -> List[Transaction]:
        """List all transactions for a given account."""
        pass
    
    @abstractmethod
    def find_transaction_by_id(self, tx_id: str) -> Transaction:
        """Retrieve a single transaction by its ID."""
        pass


# Application Services
class AccountCreationService:
    def __init__(self, account_repo: AccountRepositoryInterface):
        self.account_repo = account_repo

    def create_account(self, account_type: str, account_id: str, owner: str, initial_deposit: float = 0.0) -> str:
        # Apply business rules
        BusinessRuleService.check_account_creation(owner, initial_deposit, account_type)
        # Instantiate domain object via Factory
        account = AccountFactory.create_account(account_type, account_id, owner, initial_deposit)
        # Persist and return ID
        return self.account_repo.create_account(account)





class TransactionService:
    def __init__(self, account_repo: AccountRepositoryInterface, transaction_repo: TransactionRepositoryInterface):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def deposit(self, account_id: str, amount: float) -> str:
        account = self.account_repo.get_account(account_id)
        account.deposit(amount)
        self.account_repo.update_account(account)
        transaction = Transaction(account_id, "DEPOSIT", amount)
        return self.transaction_repo.save_transaction(transaction)

    def withdraw(self, account_id: str, amount: float) -> str:
        account = self.account_repo.get_account(account_id)
        account.withdraw(amount)
        self.account_repo.update_account(account)
        transaction = Transaction(account_id, "WITHDRAW", amount)
        return self.transaction_repo.save_transaction(transaction)

    def get_transactions(self, account_id: str) -> List[Transaction]:
        return self.transaction_repo.list_transactions(account_id)
    
    def get_transaction(self, tx_id: str) -> Transaction:
        """Fetch a single transaction by ID."""
        return self.transaction_repo.find_transaction_by_id(tx_id)


