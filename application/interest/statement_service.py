from abc import ABC, abstractmethod
from datetime import date
from domain.interest.statement import MonthlyStatement

# StatementService interface
class StatementServiceInterface(ABC):
    @abstractmethod
    def generate_statement(
        self, account_id: str, year: int, month: int, as_of: date
    ) -> MonthlyStatement:
        """Generate a monthly statement for the specified account and period."""
        pass
