from typing import List
from domain.accounts.transaction import Transaction
from application.transfer_logging.logging_service import LoggerInterface


class ConsoleLogger(LoggerInterface):
    """Simple console-based logger."""
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")

        
class TransactionServiceLogger:
    """
    Concrete decorator for TransactionService that adds logging.
    """
    def __init__(self, wrapped_service, logger: LoggerInterface):
        self._service = wrapped_service
        self._logger = logger

    def deposit(self, account_id: str, amount: float) -> str:
        tx_id = self._service.deposit(account_id, amount)
        self._logger.log(f"Deposit of {amount} to {account_id}, tx_id={tx_id}")
        return tx_id

    def withdraw(self, account_id: str, amount: float) -> str:
        tx_id = self._service.withdraw(account_id, amount)
        self._logger.log(f"Withdraw of {amount} from {account_id}, tx_id={tx_id}")
        return tx_id

    def get_transactions(self, account_id: str) -> List[Transaction]:
        self._logger.log(f"Fetching transactions for {account_id}")
        return self._service.get_transactions(account_id)

    def get_transaction(self, tx_id: str) -> Transaction:
        self._logger.log(f"Fetching transaction {tx_id}")
        return self._service.get_transaction(tx_id)
