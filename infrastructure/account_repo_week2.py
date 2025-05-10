from typing import Dict
from application.services import AccountRepositoryInterface
from domain.accounts.create_accounts import Account


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
    
    def update_accounts(self, source: Account, dest: Account) -> None:

        """
        Atomically update both source and destination accounts.
        In a real DB this would be in a transaction.
        """
         
        if source.account_id not in self._accounts or dest.account_id not in self._accounts:
            raise KeyError("One or both accounts not found")
        self._accounts[source.account_id] = source
        self._accounts[dest.account_id] = dest

