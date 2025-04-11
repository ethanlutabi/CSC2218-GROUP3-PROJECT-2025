class Account:
    def _init_(self, account_id: int, account_type: str, balance: float):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance