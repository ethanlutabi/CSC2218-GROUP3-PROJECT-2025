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
