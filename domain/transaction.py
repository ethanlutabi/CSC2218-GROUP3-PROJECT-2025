# # this file defines the Transaction class and its properties
# from dataclasses import dataclass
# from enum import Enum, auto
# from datetime import datetime

# class TransactionType(Enum):
#     DEPOSIT = auto()
#     WITHDRAW = auto()


# @dataclass
# class Transaction:
#     transaction_id: str
#     transaction_type: TransactionType
#     amount: float
#     timestamp: datetime
#     account_id: str

from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class TransactionType(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()
    TRANSFER = auto()

@dataclass
class Transaction:
    transaction_id: str
    transaction_type: TransactionType
    amount: float
    timestamp: datetime
    account_id: str  # For transfers, this is the source account
    destination_account_id: Optional[str] = None