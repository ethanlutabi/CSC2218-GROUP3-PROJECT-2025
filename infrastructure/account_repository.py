# this file defines the account respository interface and its in-memory implementation
from typing import Dict, Optional
from domain.account import Account
from threading import Lock

class InMemoryAccountRepository:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
    
    def create_account(self, account: Account) -> str:
        self.accounts[account.account_id] = account
        return account.account_id
    
    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)
    
    def update_account(self, account: Account) -> None:
        if account.account_id not in self.accounts:
            raise ValueError("Account does not exist")
        self.accounts[account.account_id] = account
        

    def __init__(self):
        self.accounts = {}
        self.lock = Lock()  # For thread safety
    
    def find_by_id(self, account_id: str):
        with self.lock:
            return self.accounts.get(account_id)
    
    def save(self, account):
        with self.lock:
            self.accounts[account.account_id] = account