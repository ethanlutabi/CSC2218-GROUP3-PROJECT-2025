
from abc import ABC, abstractmethod
from datetime import date
from typing import List


class InterestServiceInterface(ABC):
    @abstractmethod
    def apply_interest_to_account(self, account_id: str, as_of: date) -> float:
        """Apply interest to a single account and return the amount applied."""
        pass

    @abstractmethod
    def apply_interest_batch(self, account_ids: List[str], as_of: date) -> List[float]:
        """Apply interest to multiple accounts; return list of interest amounts."""
        pass

    @abstractmethod
    def calculate_interest_preview(self, account_id: str, as_of: date) -> float:
        """Calculate interest for an account without modifying its state (preview)."""
        pass

    @abstractmethod
    def set_interest_strategy(self, account_id: str, strategy_id: str) -> None:
        """Assign or update the interest strategy for a given account."""
        pass
