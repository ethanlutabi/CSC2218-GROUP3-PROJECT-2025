class BusinessRuleService:
    @staticmethod
    def check_account_creation(owner: str, initial_deposit: float, account_type: str):
        if not owner:
            raise ValueError("Account owner name is required")
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        if account_type not in ("savings", "checking"):
            raise ValueError("Invalid account type")

