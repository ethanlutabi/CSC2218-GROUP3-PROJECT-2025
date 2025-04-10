class Transaction:
    def _init_(self, transaction_id: int, account_id: int, amount: float, transaction_type: str):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type