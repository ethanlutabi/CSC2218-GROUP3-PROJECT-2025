# domain/interest/limit_constraint.py
from dataclasses import dataclass
from datetime import date


@dataclass
class LimitConstraint:
    daily_limit: float | None = None
    monthly_limit: float | None = None
    daily_used: float = 0.0
    monthly_used: float = 0.0
    last_record_date: date | None = None


    def check(self, amount: float, on_date: date) -> None:
        # reset counters if day or month changed
        if self.last_record_date != on_date:
            if self.last_record_date is None or on_date.month != self.last_record_date.month:
                self.monthly_used = 0.0
            self.daily_used = 0.0
            self.last_record_date = on_date
        if self.daily_limit is not None and self.daily_used + amount > self.daily_limit:
            raise ValueError("Daily limit exceeded")
        if self.monthly_limit is not None and self.monthly_used + amount > self.monthly_limit:
            raise ValueError("Monthly limit exceeded")

    def record(self, amount: float, on_date: date) -> None:
        # assume check already passed
        if self.last_record_date != on_date:
            if self.last_record_date is None or on_date.month != self.last_record_date.month:
                self.monthly_used = 0.0
            self.daily_used = 0.0
            self.last_record_date = on_date
        self.daily_used += amount
        self.monthly_used += amount