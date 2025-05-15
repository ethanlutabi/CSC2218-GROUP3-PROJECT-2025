from create_accounts import Account


class SavingsAccount(Account):
    def account_type(self) -> str:
        return "savings"