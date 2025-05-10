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

    
