# domain/entities/transaction.py

from enum import Enum
import uuid
from datetime import datetime


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Transaction:
    def __init__(self, transaction_type: TransactionType, amount: float, account_id: str):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")

        self.transaction_id = str(uuid.uuid4())
        self.transaction_type = transaction_type
        self.amount = amount
        self.timestamp = datetime.now(datetime.UTC)
        self.account_id = account_id

    def is_deposit(self) -> bool:
        return self.transaction_type == TransactionType.DEPOSIT

    def is_withdrawal(self) -> bool:
        return self.transaction_type == TransactionType.WITHDRAW

    def __repr__(self):
        return (
            f"<Transaction(id={self.transaction_id}, "
            f"type={self.transaction_type.value}, "
            f"amount={self.amount}, "
            f"account_id={self.account_id}, "
            f"timestamp={self.timestamp.isoformat()})>"
        )
