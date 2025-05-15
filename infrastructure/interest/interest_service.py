# infrastructure/week3/implementations.py
from datetime import date
from domain.accounts.create_accounts import Account
from application.interest.interest_strategy_interface import InterestStrategyRepositoryInterface
from application.interest.interest_service import InterestServiceInterface
from application.services import AccountRepositoryInterface
from domain.interest.interest_service import InterestService as DomainInterestService

from infrastructure.account_repo import InMemoryAccountRepository


class InterestServiceImpl(InterestServiceInterface):
    """
    Concrete implementation of InterestServiceInterface.
    Depends on injected AccountRepositoryInterface and InterestStrategyRepositoryInterface.
    """
    def __init__(
        self,
        account_repo: AccountRepositoryInterface,
        strategy_repo: InterestStrategyRepositoryInterface
    ):
        # Repositories are injected, no new() inside methods
        self.account_repo = account_repo
        self.strategy_repo = strategy_repo

    def apply_interest_to_account(self, account_id: str, as_of: date) -> float:
        # Use repository to retrieve account
        account: Account = self.account_repo.get_account(account_id)
        # Assign strategy if not already set
        if not account.interest_strategy:
            strategy = self.strategy_repo.get_strategy(account.account_type())
            account.interest_strategy = strategy
        # Delegate to domain service
        interest_amount = DomainInterestService.apply_interest(account, as_of)
        # Persist via repository
        self.account_repo.update_account(account)
        return interest_amount

    def apply_interest_batch(self, account_ids, as_of: date):
        return [self.apply_interest_to_account(aid, as_of) for aid in account_ids]

    def calculate_interest_preview(self, account_id: str, as_of: date) -> float:
        account: Account = self.account_repo.get_account(account_id)
        strategy = account.interest_strategy or self.strategy_repo.get_strategy(account.account_type())
        # Do not modify account state
        return strategy.calculate_interest(account, as_of)

    def set_interest_strategy(self, account_id: str, strategy_id: str) -> None:
        account: Account = self.account_repo.get_account(account_id)
        strategy = self.strategy_repo.get_strategy(strategy_id)
        account.interest_strategy = strategy
        self.account_repo.update_account(account)
