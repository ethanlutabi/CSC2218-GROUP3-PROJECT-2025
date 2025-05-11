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


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, req: TransactionRequest):
    try:
        tx_id = transaction_service.deposit(account_id, req.amount)
        return {"transaction_id": tx_id}
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, req: TransactionRequest):
    try:
        tx_id = transaction_service.withdraw(account_id, req.amount)
        return {"transaction_id": tx_id}
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


