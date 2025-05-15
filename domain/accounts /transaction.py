from uuid import uuid4
from datetime import datetime, timezone

class Transaction:
    def __init__(
        self,
        account_id: str,
        transaction_type: str,  # e.g. "DEPOSIT" or "WITHDRAW"
        amount: float,
    ):
        self.transaction_id = str(uuid4())
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now(timezone.utc)

    def __repr__(self):
        return (
            f"<Transaction "
            f"id={self.transaction_id} "
            f"type={self.transaction_type} "
            f"amount={self.amount} "
            f"account={self.account_id} "
            f"time={self.timestamp.isoformat()}>"
        )
