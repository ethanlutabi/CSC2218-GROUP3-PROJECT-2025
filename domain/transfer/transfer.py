# domain/transfer/transfer.py
from domain.accounts.transaction import Transaction

class TransferTransaction(Transaction):
    """
    Represents a transfer transaction between two accounts.
    Inherits common fields (transaction_id, timestamp) from Transaction.
    """
    def __init__(self, source_account_id: str, dest_account_id: str, amount: float):
        # Use source_account_id as the 'account' field for the base Transaction constructor
        super().__init__(account_id=source_account_id, transaction_type="TRANSFER", amount=amount)
        self.source_account_id = source_account_id
        self.dest_account_id = dest_account_id

    def __repr__(self):
        return (
            f"<TransferTransaction id={self.transaction_id} "
            f"from={self.source_account_id} to={self.dest_account_id} "
            f"amount={self.amount} time={self.timestamp.isoformat()}>"
        )
