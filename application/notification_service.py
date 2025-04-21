from abc import ABC, abstractmethod
from domain.transaction import Transaction, TransactionType
from domain.account import Account

class NotificationAdapter(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

class NotificationService:
    def __init__(self, account_repo, adapters: list[NotificationAdapter]):
        self.account_repo = account_repo
        self.adapters = adapters
    
    def notify_transaction(self, transaction: Transaction):
        account = self.account_repo.find_by_id(transaction.account_id)
        if not account or not account.owner_id:
            return False
        
        message = self._format_message(transaction)
        results = [adapter.send(account.owner_id, message) for adapter in self.adapters]
        return any(results)
    
    def _format_message(self, transaction) -> str:
        if transaction.transaction_type == TransactionType.TRANSFER:
            return (f"Transfer of ${transaction.amount:.2f} from account {transaction.account_id} "
                   f"to {transaction.destination_account_id}")
        else:
            action = "Deposit" if transaction.transaction_type == TransactionType.DEPOSIT else "Withdrawal"
            return f"{action} of ${transaction.amount:.2f} on account {transaction.account_id}"