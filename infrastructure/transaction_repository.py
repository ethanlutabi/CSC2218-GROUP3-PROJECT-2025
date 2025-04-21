# # this file defines the Transaction repository interface and its in-memory implementation
# from typing import Dict, List, Optional
# from domain.transaction import Transaction

# class InMemoryTransactionRepository:
#     def __init__(self):
#         self.transactions: Dict[str, Transaction] = {}
#         self.account_transactions: Dict[str, List[str]] = {}
    
#     def save_transaction(self, transaction: Transaction) -> str:
#         self.transactions[transaction.transaction_id] = transaction
        
#         if transaction.account_id not in self.account_transactions:
#             self.account_transactions[transaction.account_id] = []
#         self.account_transactions[transaction.account_id].append(transaction.transaction_id)
        
#         return transaction.transaction_id
    
#     def get_transactions_for_account(self, account_id: str) -> List[Transaction]:
#         if account_id not in self.account_transactions:
#             return []
        
#         return [
#             self.transactions[tx_id] 
#             for tx_id in self.account_transactions[account_id]
#         ]

from typing import Dict, List, Optional
from domain.transaction import Transaction

class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.account_transactions: Dict[str, List[str]] = {}
    
    def save_transaction(self, transaction: Transaction) -> str:
        """Original method name kept for backward compatibility"""
        return self.save(transaction)
    
    def save(self, transaction: Transaction) -> str:
        """New standard method name that services will use"""
        self.transactions[transaction.transaction_id] = transaction
        
        if transaction.account_id not in self.account_transactions:
            self.account_transactions[transaction.account_id] = []
        self.account_transactions[transaction.account_id].append(transaction.transaction_id)
        
        # For transfers, add to destination account's history too
        if hasattr(transaction, 'destination_account_id') and transaction.destination_account_id:
            if transaction.destination_account_id not in self.account_transactions:
                self.account_transactions[transaction.destination_account_id] = []
            self.account_transactions[transaction.destination_account_id].append(transaction.transaction_id)
        
        return transaction.transaction_id
    
    def get_transactions_for_account(self, account_id: str) -> List[Transaction]:
        """Get all transactions for a specific account"""
        if account_id not in self.account_transactions:
            return []
        
        return [
            self.transactions[tx_id] 
            for tx_id in self.account_transactions[account_id]
        ]
    
    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        """Find a specific transaction by ID"""
        return self.transactions.get(transaction_id)