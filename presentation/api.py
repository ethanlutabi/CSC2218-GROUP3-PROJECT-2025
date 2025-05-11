from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from infrastructure.account_repo import InMemoryAccountRepository
from infrastructure.transaction_repo import InMemoryTransactionRepository
from application.services import AccountCreationService
from application.__init__ import TransactionService

# Request schemas
class CreateAccountRequest(BaseModel):
    account_type: str
    account_id: str
    owner: str
    initial_deposit: float = 0.0

class TransactionRequest(BaseModel):
    amount: float

# FastAPI app initialization
app = FastAPI()





# Infrastructure -> Application wiring
account_repo = InMemoryAccountRepository()
transaction_repo = InMemoryTransactionRepository()
account_service = AccountCreationService(account_repo)
transaction_service = TransactionService(account_repo, transaction_repo)



# Presentation Layer Endpoints
@app.post("/accounts")
def create_account(req: CreateAccountRequest):
    try:
        account_id = account_service.create_account(
            req.account_type, req.account_id, req.owner, req.initial_deposit
        )
        return {"account_id": account_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))





# Pydantic models for API
class AccountType(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER = "TRANSFER"
    
    
 
'''THIS IS WEEK TWO WORK'''   
class TransferType(str, Enum):
    EMAIL = "email"
    SMS = "sms"

class CreateAccountRequest(BaseModel):
    account_type: AccountType
    initial_deposit: float = 0.0

class AccountResponse(BaseModel):
    account_id: str
    account_type: AccountType
    balance: float
    status: str
    creation_date: datetime

class TransactionRequest(BaseModel):
    amount: float

'''THIS IS WEEK TWO WORK'''
class TransferRequest(BaseModel): 
    source_account_id: str
    destination_account_id: str
    amount: float
'''THIS IS WEEK TWO WORK'''
class NotificationPreferenceRequest(BaseModel):
    notify_type: TransferType
    enabled: bool

class TransactionResponse(BaseModel):
    transaction_id: str
    transaction_type: TransactionType
    amount: float
    timestamp: datetime
    account_id: str

# Helper functions for mapping between domain and API models
def map_account_type(domain_type: DomainAccountType) -> AccountType:
    return AccountType.CHECKING if domain_type == DomainAccountType.CHECKING else AccountType.SAVINGS

def map_account_status(domain_status: DomainAccountStatus) -> str:
    return "ACTIVE" if domain_status == DomainAccountStatus.ACTIVE else "CLOSED"

def map_transaction_type(domain_type: DomainTransactionType) -> TransactionType:
    return TransactionType.DEPOSIT if domain_type == DomainTransactionType.DEPOSIT else TransactionType.WITHDRAW

# API Endpoints
@app.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(request: CreateAccountRequest):
    try:
        domain_account_type = (
            DomainAccountType.CHECKING 
            if request.account_type == AccountType.CHECKING 
            else DomainAccountType.SAVINGS
        )
        
        account_id = account_creation_service.create_account(
            domain_account_type, 
            request.initial_deposit,
            owner_id="user123"
        )
        
        account = account_repo.get_account_by_id(account_id)
        return AccountResponse(
            account_id=account.account_id,
            account_type=map_account_type(account.account_type),
            balance=account.balance,
            status=map_account_status(account.status),
            creation_date=account.creation_date
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/deposit", response_model=TransactionResponse)
def deposit(account_id: str, request: TransactionRequest):
    try:
        transaction = transaction_service.deposit(account_id, request.amount)
        return TransactionResponse(
            transaction_id=transaction.transaction_id,
            transaction_type=map_transaction_type(transaction.transaction_type),
            amount=transaction.amount,
            timestamp=transaction.timestamp,
            account_id=transaction.account_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/withdraw", response_model=TransactionResponse)
def withdraw(account_id: str, request: TransactionRequest):
    try:
        transaction = transaction_service.withdraw(account_id, request.amount)
        return TransactionResponse(
            transaction_id=transaction.transaction_id,
            transaction_type=map_transaction_type(transaction.transaction_type),
            amount=transaction.amount,
            timestamp=transaction.timestamp,
            account_id=transaction.account_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts/{account_id}/balance", response_model=dict)
def get_balance(account_id: str):
    account = account_repo.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": account.balance, "available_balance": account.balance}

@app.get("/accounts/{account_id}/transactions", response_model=List[TransactionResponse])
def get_transactions(account_id: str):
    transactions = transaction_repo.get_transactions_for_account(account_id)
    return [
        TransactionResponse(
            transaction_id=t.transaction_id,
            transaction_type=map_transaction_type(t.transaction_type),
            amount=t.amount,
            timestamp=t.timestamp,
            account_id=t.account_id
        )
        for t in transactions
    ]
    
    
    # Transfer endpoint WEEK TWO WORK
    
@app.post("/transfers", response_model=TransactionResponse)
def create_transfer(request: TransferRequest):
    try:
        transaction = fund_transfer_service.transfer_funds(
            request.source_account_id,
            request.destination_account_id,
            request.amount
        )
        
        # Send notification
        notification_service.notify_transaction(transaction)
        
        return TransactionResponse(
            transaction_id=transaction.transaction_id,
            transaction_type=map_transaction_type(transaction.transaction_type),
            amount=transaction.amount,
            timestamp=transaction.timestamp,
            account_id=transaction.account_id,
            destination_account_id=transaction.destination_account_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/notification-preferences", status_code=201)
def set_notification_preferences(
    account_id: str, 
    request: NotificationPreferenceRequest
):
    # In a real implementation, you would save these preferences to a database
    return {
        "account_id": account_id,
        "notify_type": request.notify_type,
        "enabled": request.enabled,
        "message": "Notification preference updated"
    }

# @app.post("/accounts/{account_id}/notification-preferences")
# def set_notification_preferences(account_id: str, request: NotificationPreferenceRequest):
#     # Simple validation
#     if request.notify_type.lower() not in ["email", "sms"]:
#         raise HTTPException(status_code=400, detail="Type must be 'email' or 'sms'")
    
#     return {
#         "status": "success",
#         "account_id": account_id,
#         "notify_type": request.notify_type,
#         "enabled": request.enabled
#     }

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str):
    transaction = transaction_repo.find_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        transaction_type=map_transaction_type(transaction.transaction_type),
        amount=transaction.amount,
        timestamp=transaction.timestamp,
        account_id=transaction.account_id,
        destination_account_id=getattr(transaction, 'destination_account_id', None)
    )

@app.get("/logs/transactions")
def get_transaction_logs():
    # In a real implementation, you would query your logging system
    return {"message": "Transaction logs would be returned here"}
