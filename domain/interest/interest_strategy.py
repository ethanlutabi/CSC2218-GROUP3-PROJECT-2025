# domain/interest/interest_strategy.py

from abc import ABC, abstractmethod
from datetime import date
from domain.accounts.create_accounts import Account

class InterestStrategy(ABC):
    @abstractmethod
    def calculate_interest(self, account: Account, as_of: date) -> float:
        """
        Compute interest earned on the account since its last calculation date,
        up to (and including) `as_of`.
        """
        pass



