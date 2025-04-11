from abc import ABC, abstractmethod
from typing import Optional
from models.accountModel import Account

class AccountRepository(ABC):
    @abstractmethod
    def create_account(self, account: Account) -> int:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> None:
        pass

class InMemoryAccountRepository(AccountRepository):
    def _init_(self):
        self.accounts = {}
        self.next_id = 1

    def create_account(self, account: Account) -> int:
        account.account_id = self.next_id
        self.accounts[self.next_id] = account
        self.next_id += 1
        return account.account_id

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        return self.accounts.get(account_id)

    def update_account(self, account: Account) -> None:
        if account.account_id in self.accounts:
            self.accounts[account.account_id] = account