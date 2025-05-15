from domain.interest import checking_interest, savings_interest, limits_constraint, limit_account
from domain.accounts.factory import AccountFactory

def test_checking_interest_calculation():
    base_account = AccountFactory.create_account("checking", "acc1", "User1", 1000)
    account = limit_account.LimitedAccount(base_account, limits_constraint.LimitConstraint())
    interest = checking_interest.CheckingInterestStrategy(annual_rate=0.01)
    calculated_interest = interest.calculate_interest(account, base_account.last_interest_date)
    assert isinstance(calculated_interest, (int, float))

def test_savings_interest_calculation():
    base_account = AccountFactory.create_account("savings", "acc2", "User2", 2000)
    account = limit_account.LimitedAccount(base_account, limits_constraint.LimitConstraint())
    interest = savings_interest.SavingsInterestStrategy(annual_rate=0.02)
    calculated_interest = interest.calculate_interest(account, base_account.last_interest_date)
    assert isinstance(calculated_interest, (int, float))

def test_limits_constraint():
    constraint = limits_constraint.LimitConstraint()
    try:
        constraint.check(100, None)
        result = True
    except Exception:
        result = False
    assert result
