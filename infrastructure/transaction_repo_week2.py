from typing import Dict, List
from application.services import TransactionRepositoryInterface
from domain.accounts.transaction import Transaction


class InMemoryTransactionRepository(TransactionRepositoryInterface):
    def __init__(self):
        # key: transaction_id, value: Transaction instance
        self._transactions: Dict[str, Transaction] = {}
        # index for quick lookup by account
        self._by_account: Dict[str, List[str]] = {}

    def save_transaction(self, transaction: Transaction) -> str:
        self._transactions[transaction.transaction_id] = transaction
        self._by_account.setdefault(transaction.account_id, []).append(transaction.transaction_id)
        return transaction.transaction_id

    def list_transactions(self, account_id: str) -> List[Transaction]:
        tx_ids = self._by_account.get(account_id, [])
        return [self._transactions[tx_id] for tx_id in tx_ids]
    
    def find_transaction_by_id(self, tx_id: str) -> Transaction:
        tx = self._transactions.get(tx_id)
        if not tx:
            raise KeyError(f"Transaction {tx_id} not found")
        return tx