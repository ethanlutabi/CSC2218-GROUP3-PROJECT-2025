from domain.accounts.create_accounts import Account
from domain.interest.interest_strategy import InterestStrategy
from datetime import date

class CheckingInterestStrategy(InterestStrategy):
    def __init__(self, annual_rate: float):
        self.annual_rate = annual_rate

    def calculate_interest(self, account: Account, as_of: date) -> float:
        days = (as_of - account.last_interest_date).days
        return account.balance * (self.annual_rate / 2) * days / 365
