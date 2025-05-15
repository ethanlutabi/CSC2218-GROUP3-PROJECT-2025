from typing import Dict
from application.interest.limit_check import LimitEnforcementServiceInterface
from domain.interest.limits_constraint import LimitConstraint
from datetime import date
from application.services import AccountRepositoryInterface

class LimitEnforcementServiceImpl(LimitEnforcementServiceInterface):



    def __init__(self, account_repo: AccountRepositoryInterface):
        self.account_repo: AccountRepositoryInterface = account_repo

    def check_limit(self, account_id: str, amount: float) -> bool:
         # Retrieve the live constraint (auto‑saves a new one if none exists)
        constraint = self.account_repo.get_constraints(account_id)
        # Perform the check (will raise if violated)
        constraint.check(amount, date.today())
        # Persist the fact that we looked it up (in case it was newly created)
        self.account_repo.save_constraints(account_id, constraint)
        return True

    def reset_limits_daily(self) -> None:
        
        for constraint in self.account_repo.get_constraint_dict().values():
            constraint.daily_used = 0.0

    def reset_limits_monthly(self) -> None:
        for constraint in self.account_repo.get_constraint_dict().values():
            constraint.monthly_used = 0.0

    def configure_limits(self, account_id: str, daily: float, monthly: float) -> None:
        # Create or update constraint for the given account
        constraint = LimitConstraint(daily_limit=daily, monthly_limit=monthly)
        constraints:Dict[str, LimitConstraint] = self.account_repo.get_constraint_dict()
        constraints[account_id] = constraint

    def get_limits(self, account_id: str) -> LimitConstraint:
        # Return existing or default constraint
        constraints:Dict[str, LimitConstraint] = self.account_repo.get_constraint_dict()
        return constraints.get(account_id, LimitConstraint())



