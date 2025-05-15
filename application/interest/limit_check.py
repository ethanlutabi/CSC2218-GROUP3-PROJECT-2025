from abc import ABC, abstractmethod

class LimitEnforcementServiceInterface(ABC):
    @abstractmethod
    def check_limit(self, account_id: str, amount: float) -> bool:
        """Check if a transaction amount is within limits for the given account."""
        pass

    @abstractmethod
    def reset_limits_daily(self) -> None:
        """Reset daily usage counters for all accounts."""
        pass

    @abstractmethod
    def reset_limits_monthly(self) -> None:
        """Reset monthly usage counters for all accounts."""
        pass