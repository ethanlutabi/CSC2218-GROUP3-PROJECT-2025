# domain/interest_service.py
from datetime import date
from domain.accounts.create_accounts import Account
from domain.interest.interest_strategy import InterestStrategy

class InterestService:
    """
    Domain service that applies interest to an account using its strategy.
    """
    @staticmethod
    def apply_interest(account: Account, as_of: date) -> float:
        if not isinstance(account.interest_strategy, InterestStrategy):
            raise ValueError("No valid interest strategy attached to account")
        # Calculate interest
        interest = account.interest_strategy.calculate_interest(account, as_of)
        # Update balance and last_interest_date
        account.balance += interest
        account.last_interest_date = as_of
        return interest

