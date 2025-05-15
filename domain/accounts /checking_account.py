from domain.accounts.create_accounts import Account
class CheckingAccount(Account):
    def account_type(self) -> str:
        return "checking"