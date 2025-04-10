from abc import ABC, abstractmethod
from typing import List
from models.transactionModel import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    def save_transaction(self, transaction: Transaction) -> int:
        pass

    @abstractmethod
    def get_transactions_for_account(self, account_id: int) -> List[Transaction]:
        pass

class InMemoryTransactionRepository(TransactionRepository):
    def _init_(self):
        self.transactions = {}
        self.next_id = 1

    def save_transaction(self, transaction: Transaction) -> int:
        transaction.transaction_id = self.next_id
        self.transactions[self.next_id] = transaction
        self.next_id += 1
        return transaction.transaction_id

    def get_transactions_for_account(self, account_id: int) -> List[Transaction]:
        return [t for t in self.transactions.values() if t.account_id == account_id]