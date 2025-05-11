# application/transfer_logging/transfer_service.py
from application.services import (
    AccountRepositoryInterface,
    TransactionRepositoryInterface,
)
from application.transfer_logging.notifications_services import NotificationAdapterInterface
from domain.transfer.transfer import TransferTransaction
from domain.transfer.transfer_service import TransferService


class FundTransferService:
    def __init__(
        self,
        account_repo: AccountRepositoryInterface,
        transaction_repo: TransactionRepositoryInterface,
        notification_adapter: NotificationAdapterInterface = None,
    ):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.notification_adapter = notification_adapter

    def transfer_funds(self, source_id: str, dest_id: str, amount: float) -> str:
        # Fetch domain objects
        source = self.account_repo.get_account(source_id)
        destination = self.account_repo.get_account(dest_id)
        # Domain-level transfer
        transfer_tx: TransferTransaction = TransferService.execute(source, destination, amount)
        # Persist updated accounts
        self.account_repo.update_accounts(source, destination)
        # Persist transaction
        tx_id = self.transaction_repo.save_transaction(transfer_tx)
        # Notify user if adapter provided
        if self.notification_adapter:
            subject = "Transfer Completed"
            body = f"Transferred {amount} from {source_id} to {dest_id}. Transaction ID: {tx_id}"
            # For simplicity, assume owner name is recipient identifier
            self.notification_adapter.send_email(source.owner, subject, body)
        return tx_id
