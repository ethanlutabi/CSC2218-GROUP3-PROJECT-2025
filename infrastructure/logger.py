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
   
    
    
    def __init__(self, app_name: str = "banking-app", log_level: int = logging.INFO):
        
        
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
       
        
        return logger
    
    def get_component_logger(self, component_name: str) -> logging.Logger:
        
        
        if component_name not in self._component_loggers:
            logger = logging.getLogger(f"{self.root_logger.name}.{component_name}")
            self._component_loggers[component_name] = logger
        
        return self._component_loggers[component_name]
    
    def log_transaction(self, 
                        transaction_type: str, 
                        transaction_id: str, 
                        details: Dict[str, Any], 
                        level: int = logging.INFO) -> None:

        extra = {
            'transaction_id': transaction_id,
            'transaction_type': transaction_type
        }
        
        # Format details as JSON
        details_json = json.dumps(details)
        self.transaction_logger.log(level, f"{transaction_type}: {details_json}", extra=extra)
    
    def log(self, level: int, message: str, transaction_id: Optional[str] = None, **kwargs) -> None:
                
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



