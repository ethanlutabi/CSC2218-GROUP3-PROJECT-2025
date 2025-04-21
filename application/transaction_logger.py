import logging
from functools import wraps
from domain.transaction import Transaction

class TransactionLogger:
    def __init__(self, logger_name='banking'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('transactions.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_transaction(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if isinstance(result, Transaction):
                    self._log_transaction_details(result)
                return result
            except Exception as e:
                self.logger.error(f"Transaction failed: {str(e)}")
                raise
        return wrapper
    
    def _log_transaction_details(self, transaction: Transaction):
        log_msg = f"Transaction {transaction.transaction_id}: "
        log_msg += f"Type={transaction.transaction_type.name}, "
        log_msg += f"Amount={transaction.amount}, "
        log_msg += f"Account={transaction.account_id}"
        
        if transaction.destination_account_id:
            log_msg += f", DestAccount={transaction.destination_account_id}"
            
        self.logger.info(log_msg)