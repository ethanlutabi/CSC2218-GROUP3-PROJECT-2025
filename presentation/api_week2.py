# THIS IS WEEK TWO SEPARATE CODE
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from infrastructure.account_repo import InMemoryAccountRepository
from infrastructure.transaction_repo import InMemoryTransactionRepository

from infrastructure.adapters.notify import ConsoleNotificationAdapter
from application.services import AccountCreationService, TransactionService
from application.transfer_logging.transfer_service import FundTransferService
from infrastructure.adapters.logging import TransactionServiceLogger, ConsoleLogger


# Pydantic schemas
class CreateAccountRequest(BaseModel):
    account_type: str
    account_id: str
    owner: str
    initial_deposit: float = 0.0

class TransactionRequest(BaseModel):
    amount: float

class TransferRequest(BaseModel):
    source_account_id: str
    destination_account_id: str
    amount: float

# Initialize app
app = FastAPI()

# Root endpoint
@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome! See /docs for API endpoints."}


# Infrastructure wiring
account_repo = InMemoryAccountRepository()
transaction_repo = InMemoryTransactionRepository()
notifier = ConsoleNotificationAdapter()
logger = ConsoleLogger()

# Application services
account_service = AccountCreationService(account_repo)
base_tx_service = TransactionService(account_repo, transaction_repo)
tx_service_with_logging = TransactionServiceLogger(base_tx_service, logger)
fund_transfer_service = FundTransferService(account_repo, transaction_repo, notification_adapter=notifier)
