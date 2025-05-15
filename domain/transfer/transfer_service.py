from domain.accounts.create_accounts import Account
from domain.transfer.transfer import TransferTransaction

class TransferService:
    """
    Domain service responsible for atomic transfer logic.
    Withdraws from source account and deposits into destination account.
    """
    @staticmethod
    def execute(source: Account, destination: Account, amount: float) -> TransferTransaction:
        # Perform domain-level operations (may raise ValueError on insufficient funds)
        source.withdraw(amount)
        destination.deposit(amount)
        # Create and return a TransferTransaction domain entity
        return TransferTransaction(source.account_id, destination.account_id, amount)
