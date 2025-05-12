from typing import Dict
from application.services import AccountRepositoryInterface
from domain.accounts import Account


class InMemoryAccountRepository(AccountRepositoryInterface):
    def __init__(self):
        # key: account_id, value: Account instance
        self._accounts: Dict[str, Account] = {}

    def create_account(self, account: Account) -> str:
        self._accounts[account.account_id] = account
        return account.account_id

    def get_account(self, account_id: str) -> Account:
        account = self._accounts.get(account_id)
        if not account:
            raise KeyError(f"Account {account_id} not found")
        return account

    def update_account(self, account: Account) -> None:
        if account.account_id not in self._accounts:
            raise KeyError(f"Account {account.account_id} not found")
        self._accounts[account.account_id] = account
    
    def transfer_between_accounts(self, source_id: str, dest_id: str, amount: float) -> None:
       
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
            
        # Get accounts (will raise KeyError if not found)
        source_account = self.get_account(source_id)
        dest_account = self.get_account(dest_id)
        
        # Check sufficient balance
        if source_account.balance < amount:
            raise ValueError(f"Insufficient funds in account {source_id}")
        
        # Update balances
        source_account.balance -= amount
        dest_account.balance += amount
        
        # Atomically update both accounts
        self.update_accounts(source_account, dest_account)

