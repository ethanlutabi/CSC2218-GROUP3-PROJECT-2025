import logging
import json
import uuid
import time
import functools
import inspect
from typing import Any, Callable, Dict, Optional, Union
from datetime import datetime

# Configure logging formats
DEFAULT_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] [%(transaction_id)s] %(message)s'
TRANSACTION_FORMAT = '%(asctime)s [%(levelname)s] [TRANSACTION] [%(transaction_id)s] [%(transaction_type)s] %(message)s'

class BankingLogger:
    """
    Central logging facility for the banking application.
    Provides both general-purpose logging and specialized transaction logging.
    """
    
    def __init__(self, app_name: str = "banking-app", log_level: int = logging.INFO):
        """
        Initialize the logger with application name and log level.
        
        Args:
            app_name: Name of the application for the root logger
            log_level: Default logging level
        """
        # Set up the root logger
        self.root_logger = logging.getLogger(app_name)
        self.root_logger.setLevel(log_level)
        
        # Create console handler if none exists
        if not self.root_logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
            self.root_logger.addHandler(console_handler)
        
        # Create specialized loggers
        self.transaction_logger = self._create_transaction_logger(app_name)
        
        # Store component loggers
        self._component_loggers = {}
    
    def _create_transaction_logger(self, app_name: str) -> logging.Logger:
        """Create a specialized logger for transaction events."""
        logger = logging.getLogger(f"{app_name}.transactions")
        
        # Add a file handler specifically for transactions if needed
        # Uncomment and configure in production
        """
        file_handler = logging.FileHandler("transactions.log")
        file_handler.setFormatter(logging.Formatter(TRANSACTION_FORMAT))
        logger.addHandler(file_handler)
        """
        
        return logger
    
    def get_component_logger(self, component_name: str) -> logging.Logger:
        """
        Get or create a logger for a specific component.
        
        Args:
            component_name: Name of the component (e.g., "account_service")
            
        Returns:
            Logger instance for the component
        """
        if component_name not in self._component_loggers:
            logger = logging.getLogger(f"{self.root_logger.name}.{component_name}")
            self._component_loggers[component_name] = logger
        
        return self._component_loggers[component_name]
    
    def log_transaction(self, 
                        transaction_type: str, 
                        transaction_id: str, 
                        details: Dict[str, Any], 
                        level: int = logging.INFO) -> None:
        """
        Log a transaction with detailed information.
        
        Args:
            transaction_type: Type of transaction (DEPOSIT, WITHDRAWAL, TRANSFER, etc.)
            transaction_id: Unique ID of the transaction
            details: Dictionary with transaction details
            level: Logging level
        """
        extra = {
            'transaction_id': transaction_id,
            'transaction_type': transaction_type
        }
        
        # Format details as JSON
        details_json = json.dumps(details)
        self.transaction_logger.log(level, f"{transaction_type}: {details_json}", extra=extra)
    
    def log(self, level: int, message: str, transaction_id: Optional[str] = None, **kwargs) -> None:
        """
        Log a general message with optional transaction ID.
        
        Args:
            level: Logging level
            message: Message to log
            transaction_id: Optional transaction ID for context
            **kwargs: Additional context to include in the log
        """
        extra = {'transaction_id': transaction_id or 'N/A'}
        self.root_logger.log(level, message, extra=extra, **kwargs)
    
    # Convenience methods
    def info(self, message: str, transaction_id: Optional[str] = None, **kwargs) -> None:
        self.log(logging.INFO, message, transaction_id, **kwargs)
    
    def error(self, message: str, transaction_id: Optional[str] = None, **kwargs) -> None:
        self.log(logging.ERROR, message, transaction_id, **kwargs)
    
    def warning(self, message: str, transaction_id: Optional[str] = None, **kwargs) -> None:
        self.log(logging.WARNING, message, transaction_id, **kwargs)
    
    def debug(self, message: str, transaction_id: Optional[str] = None, **kwargs) -> None:
        self.log(logging.DEBUG, message, transaction_id, **kwargs)


# Decorator for method logging
def log_method_call(logger: Optional[Union[BankingLogger, logging.Logger]] = None, 
                   level: int = logging.DEBUG):
    """
    Decorator to log method calls with parameters and return values.
    
    Args:
        logger: Logger to use (if None, gets a new logger based on the class name)
        level: Logging level for the messages
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get appropriate logger
            nonlocal logger
            if logger is None:
                # Try to get class name if it's a method
                if args and hasattr(args[0], '__class__'):
                    component = args[0].__class__.__name__.lower()
                    logger = banking_logger.get_component_logger(component)
                else:
                    logger = banking_logger.root_logger
            
            # Get actual logger object if BankingLogger was provided
            log_obj = logger.root_logger if isinstance(logger, BankingLogger) else logger
            
            # Generate a unique ID for this call
            call_id = str(uuid.uuid4())[:8]
            
            # Get function signature and arguments
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Filter out sensitive data
            safe_args = {}
            for k, v in bound_args.arguments.items():
                if k in ('password', 'pin', 'secret'):
                    safe_args[k] = '******'
                else:
                    safe_args[k] = v
            
            # Remove 'self' from logged arguments
            if 'self' in safe_args:
                del safe_args['self']
            
            # Log method entry
            log_obj.log(level, 
                      f"CALL {func.__qualname__} START [id={call_id}] args={safe_args}", 
                      extra={'transaction_id': 'N/A'})
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                
                # Log successful completion
                duration = time.time() - start_time
                log_obj.log(level, 
                          f"CALL {func.__qualname__} END [id={call_id}] duration={duration:.4f}s result={result}", 
                          extra={'transaction_id': 'N/A'})
                return result
            except Exception as e:
                # Log exception
                duration = time.time() - start_time
                log_obj.log(logging.ERROR, 
                          f"CALL {func.__qualname__} ERROR [id={call_id}] duration={duration:.4f}s exception={str(e)}", 
                          extra={'transaction_id': 'N/A'})
                raise
        
        return wrapper
    
    return decorator


# Create a singleton instance
banking_logger = BankingLogger()


# Example usage:
"""
# Get component logger
account_logger = banking_logger.get_component_logger("account_service")

# Log regular message
banking_logger.info("Application started")

# Log with transaction ID
banking_logger.info("Processing deposit", transaction_id="tx123")

# Log transaction
banking_logger.log_transaction(
    transaction_type="DEPOSIT",
    transaction_id="tx123",
    details={"account_id": "acc456", "amount": 100.00}
)

# Use decorator
@log_method_call()
def process_transaction(tx_id, amount):
    return f"Processed {amount} for {tx_id}"

# Or with specific logger
@log_method_call(logger=account_logger)
def create_account(user_id, initial_balance):
    return f"Created account for {user_id}"
"""
