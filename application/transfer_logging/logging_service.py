# application/transfer_logging/logging_service.py
from abc import ABC, abstractmethod


# Logger interface
class LoggerInterface(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass



