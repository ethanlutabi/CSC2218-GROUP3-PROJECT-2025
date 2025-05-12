from typing import Dict, Optional, List
from datetime import date, datetime
from domain.accounts import Account

class InMemoryAccountRepository:
    def __init__(self):
        # Existing code...
        self._accounts: Dict[str, Account] = {}
        # Added for interest rates
        self._interest_rates: Dict[str, float] = {"SAVINGS": 0.025, "CHECKING": 0.005}
        # Added for transaction limits
        self._daily_limits: Dict[str, Dict[str, float]] = {}
        self._monthly_limits: Dict[str, Dict[str, float]] = {}
    
    # Existing methods...
    
    # Added for interest implementation
    def get_interest_rate(self, account_type: str) -> float:
        """Get the current interest rate for an account type."""
        return self._interest_rates.get(account_type, 0.0)
    
    def set_interest_rate(self, account_type: str, rate: float) -> None:
        """Update interest rate for an account type."""
        self._interest_rates[account_type] = rate
    
    # Added for transaction limits
    def get_daily_usage(self, account_id: str, transaction_type: str, current_date: Optional[date] = None) -> float:
        """Get the daily usage for a specific transaction type."""
        current_date = current_date or date.today()
        date_str = current_date.isoformat()
        return self._daily_limits.get(account_id, {}).get(f"{transaction_type}_{date_str}", 0.0)
    
    def update_daily_usage(self, account_id: str, transaction_type: str, amount: float) -> None:
        """Update the daily usage for a transaction type."""
        date_str = date.today().isoformat()
        key = f"{transaction_type}_{date_str}"
        
        if account_id not in self._daily_limits:
            self._daily_limits[account_id] = {}
        
        current = self._daily_limits[account_id].get(key, 0.0)
        self._daily_limits[account_id][key] = current + amount
    
    def get_monthly_usage(self, account_id: str, transaction_type: str, month: Optional[int] = None, year: Optional[int] = None) -> float:
        """Get the monthly usage for a specific transaction type."""
        today = datetime.today()
        month = month or today.month
        year = year or today.year
        key = f"{transaction_type}_{year}_{month}"
        
        return self._monthly_limits.get(account_id, {}).get(key, 0.0)
    
    def update_monthly_usage(self, account_id: str, transaction_type: str, amount: float) -> None:
        """Update the monthly usage for a transaction type."""
        today = datetime.today()
        key = f"{transaction_type}_{today.year}_{today.month}"
        
        if account_id not in self._monthly_limits:
            self._monthly_limits[account_id] = {}
        
        current = self._monthly_limits[account_id].get(key, 0.0)
        self._monthly_limits[account_id][key] = current + amount
