# application/transfer_logging/notifications_services.py
from abc import ABC, abstractmethod
from domain.accounts.create_accounts import Account
from domain.accounts.transaction import Transaction



# Notification Adapter interface
class NotificationAdapterInterface(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str) -> None:
        pass

    @abstractmethod
    def send_sms(self, number: str, message: str) -> None:
        pass



# NotificationService (Observer/Event)
class NotificationService:
    def __init__(self, adapter: NotificationAdapterInterface):
        self.adapter = adapter

    def notify(self, transaction: Transaction) -> None:
        subject = f"Transaction {transaction.transaction_type}"
        body = f"Your account {transaction.account_id} had a {transaction.transaction_type} of {transaction.amount}"
        # Send email; real implementation could choose SMS or email
        self.adapter.send_email(transaction.account_id, subject, body)
