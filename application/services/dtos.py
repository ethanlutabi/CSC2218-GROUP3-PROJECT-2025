from typing import Optional
from pydantic import BaseModel  # type: ignore

class CreateAccountDTO(BaseModel):
    """Data Transfer Object for account creation"""
    account_type: str  # "CHECKING" or "SAVINGS"
    initial_deposit: float = 0.0

class TransactionDTO(BaseModel):
    """Data Transfer Object for transactions"""
    account_id: str
    amount: float

class AccountBalanceDTO(BaseModel):
    """Data Transfer Object for account balance"""
    account_id: str
    balance: float
    available_balance: float

class TransactionHistoryDTO(BaseModel):
    """Data Transfer Object for transaction history"""
    account_id: str
    transactions: list  # List of Transaction entities