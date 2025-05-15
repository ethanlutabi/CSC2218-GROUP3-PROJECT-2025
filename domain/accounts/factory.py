from domain.accounts.checking_account import CheckingAccount
from domain.accounts.savings_account import SavingsAccount
from domain.accounts.create_accounts import Account


class AccountFactory:
    @staticmethod
    def create_account(account_type: str, account_id: str, owner: str, balance: float = 0.0) -> Account:
        if account_type == "savings":
            return SavingsAccount(account_id, owner, balance)
        elif account_type == "checking":
            return CheckingAccount(account_id, owner, balance)
        else:
            raise ValueError(f"Unknown account type: {account_type}")