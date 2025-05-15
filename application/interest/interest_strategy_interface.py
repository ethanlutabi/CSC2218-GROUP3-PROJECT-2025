from abc import ABC, abstractmethod
from domain.interest.interest_strategy import InterestStrategy

class InterestStrategyRepositoryInterface(ABC):
    @abstractmethod
    def get_strategy(self, strategy_id: str) -> InterestStrategy:
        """Fetch a configured InterestStrategy by its ID."""
        pass
