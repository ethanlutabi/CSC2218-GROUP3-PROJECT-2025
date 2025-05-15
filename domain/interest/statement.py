# domain/interest/statement.py
from dataclasses import dataclass
from datetime import date
from domain.accounts.transaction import Transaction

@dataclass
class MonthlyStatement:
    account_id: str
    year: int
    month: int
    opening_balance: float
    closing_balance: float
    interest_earned: float
    transactions: list[Transaction]
    generated_on: date
