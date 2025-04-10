from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

class AccountStatus(Enum):
    """Enum for account status (State Pattern could be added later)"""
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class AccountType(Enum):
    """Enum for account types (Strategy Pattern)"""
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

class AccountBehavior(ABC):
    """Strategy interface for account type-specific behavior"""
    @abstractmethod
    def validate_balance(self, balance: float) -> bool:
        """Validate if balance meets account type requirements"""
        pass

    @abstractmethod
    def calculate_available_balance(self, balance: float) -> float:
        """Calculate available balance (may differ from actual balance)"""
        pass

class CheckingAccountBehavior(AccountBehavior):
    """Concrete strategy for checking accounts"""
    def validate_balance(self, balance: float) -> bool:
        """Checking accounts can have negative balance (overdraft)"""
        return True
    
    def calculate_available_balance(self, balance: float) -> float:
        """Available balance same as actual balance for checking"""
        return balance

class SavingsAccountBehavior(AccountBehavior):
    """Concrete strategy for savings accounts"""
    MIN_BALANCE = 100.00  # Example minimum balance requirement
    
    def validate_balance(self, balance: float) -> bool:
        """Savings accounts cannot go below minimum balance"""
        return balance >= self.MIN_BALANCE
    
    def calculate_available_balance(self, balance: float) -> float:
        """Available balance is actual balance minus minimum requirement"""
        return max(0, balance - self.MIN_BALANCE)

class Account:
    """Domain entity representing a bank account (Aggregate Root)"""
    def __init__(
        self,
        account_id: str,
        account_type: AccountType,
        balance: float = 0.0,
        status: AccountStatus = AccountStatus.ACTIVE,
        creation_date: datetime = datetime.now()
    ):
        self.account_id = account_id
        self.account_type = account_type
        self._balance = balance
        self.status = status
        self.creation_date = creation_date
        self._behavior = self._create_behavior()
        
        # Validate initial balance
        if not self._behavior.validate_balance(self._balance):
            raise ValueError(f"Initial balance invalid for {account_type.value} account")

    def _create_behavior(self) -> AccountBehavior:
        """Factory Method pattern to create appropriate behavior"""
        if self.account_type == AccountType.CHECKING:
            return CheckingAccountBehavior()
        elif self.account_type == AccountType.SAVINGS:
            return SavingsAccountBehavior()
        else:
            raise ValueError(f"Unsupported account type: {self.account_type}")

    @property
    def balance(self) -> float:
        """Get current balance"""
        return self._balance

    @property
    def available_balance(self) -> float:
        """Get available balance according to account type rules"""
        return self._behavior.calculate_available_balance(self._balance)

    def update_balance(self, amount: float) -> None:
        """Update balance with validation"""
        new_balance = self._balance + amount
        if not self._behavior.validate_balance(new_balance):
            raise ValueError(f"Invalid balance update for {self.account_type.value} account")
        self._balance = new_balance

    def close(self) -> None:
        """Close the account"""
        self.status = AccountStatus.CLOSED