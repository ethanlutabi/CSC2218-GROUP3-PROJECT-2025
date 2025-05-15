# main.py

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Domain & Infrastructure imports
from infrastructure.account_repo import InMemoryAccountRepository
from infrastructure.transaction_repo import InMemoryTransactionRepository
from infrastructure.interest.interest_repo import ConfigInterestStrategyRepository
from infrastructure.interest.interest_service import InterestServiceImpl
from infrastructure.interest.limit_service import LimitEnforcementServiceImpl
from infrastructure.interest.statementgenerator import StatementServiceImpl
from infrastructure.interest.csv_statement_adapter import CsvStatementAdapter
from infrastructure.interest.pdf_statement_adapter import PdfStatementAdapter


# Application-layer service imports
from application.services import AccountCreationService, TransactionService
from application.transfer_logging.transfer_service import FundTransferService
from application.interest.statement_service import StatementServiceInterface

# Pydantic request schemas

class CreateAccountRequest(BaseModel):
    account_type: str
    account_id: str
    owner: str
    initial_deposit: float = 0.0

class AmountRequest(BaseModel):
    amount: float

class TransferRequest(BaseModel):
    source_account_id: str
    destination_account_id: str
    amount: float

class InterestRequest(BaseModel):
    calculationDate: date

class PreviewRequest(BaseModel):
    calculationDate: date

class LimitsConfig(BaseModel):
    dailyLimit: float
    monthlyLimit: float

# Instantiate repositories
account_repo     = InMemoryAccountRepository()
transaction_repo = InMemoryTransactionRepository()

# Week 1 services
account_service = AccountCreationService(account_repo)
tx_service      = TransactionService(account_repo, transaction_repo)

# Week 2: logging decorator and notifications (if any)
# If you have a logger decorator, wrap tx_service here.

# Transfer service
transfer_service = FundTransferService(
    account_repo,
    transaction_repo,
    notification_adapter=None  # or your concrete adapter
)

# Week 3 services
strategy_repo = ConfigInterestStrategyRepository()  # reads config/interest_rates.json
interest_service = InterestServiceImpl(account_repo, strategy_repo)
limit_service    = LimitEnforcementServiceImpl(account_repo)
statement_service = StatementServiceImpl(account_repo, transaction_repo)

# Statement adapters
csv_adapter = CsvStatementAdapter()
pdf_adapter = PdfStatementAdapter()


app = FastAPI()
@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Banking API. See /docs for usage."}

@app.post("/accounts", status_code=201)
def create_account(req: CreateAccountRequest):
    try:
        account_id = account_service.create_account(
    req.account_type, req.account_id, req.owner, req.initial_deposit
)
        return {"account_id": account_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, req: AmountRequest):
    try:
        tx_id = tx_service.deposit(account_id, req.amount)
        return {"transaction_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, req: AmountRequest):
    try:
        tx_id = tx_service.withdraw(account_id, req.amount)
        return {"transaction_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    acct = account_repo.get_account(account_id)
    return {"balance": acct.balance}


@app.get("/accounts/{account_id}/transactions")
def list_transactions(account_id: str):
    txs = transaction_repo.list_transactions_for_account(account_id)
    # convert domain Transaction to dicts
    return [
        {
            "transaction_id": t.transaction_id,
            "transaction_type": t.transaction_type,
            "amount": t.amount,
            "timestamp": t.timestamp.isoformat(),
        }
        for t in txs
    ]


@app.post("/accounts/transfer")
def transfer(req: TransferRequest):
    try:
        tx_id = transfer_service.transfer_funds(
            req.source_account_id, req.destination_account_id, req.amount
        )
        return {"transaction_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# --- Week 3 Endpoints ---

@app.post("/accounts/{account_id}/interest/calculate")
def calculate_interest(account_id: str, req: InterestRequest):
    try:
        interest = interest_service.apply_interest_to_account(account_id, req.calculationDate)
        return {"interest": interest}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/accounts/{account_id}/interest/preview")
def preview_interest(account_id: str, req: PreviewRequest):
    try:
        interest = interest_service.calculate_interest_preview(account_id, req.calculationDate)
        return {"interest": interest}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/accounts/{account_id}/limits")
def configure_limits(account_id: str, cfg: LimitsConfig):
    try:
        limit_service.configure_limits(account_id, cfg.dailyLimit, cfg.monthlyLimit)
        saved = account_repo.get_constraints(account_id)
        return {
            "dailyLimit": saved.daily_limit,
            "monthlyLimit": saved.monthly_limit,
            "dailyUsed": saved.daily_used,
            "monthlyUsed": saved.monthly_used,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/accounts/{account_id}/limits")
def get_limits(account_id: str):
    c = account_repo.get_constraints(account_id)
    return {
        "dailyLimit": c.daily_limit,
        "monthlyLimit": c.monthly_limit,
        "dailyUsed": c.daily_used,
        "monthlyUsed": c.monthly_used,
    }


@app.get("/accounts/{account_id}/statement")
def get_statement(
    account_id: str,
    year: int,
    month: int,
    format: Optional[str] = "json"
):
    try:
        stmt = statement_service.generate_statement(account_id, year, month, date.today())
        if format.lower() == "csv":
            data = csv_adapter.render(stmt)
            return Response(content=data, media_type="text/csv")
        elif format.lower() == "pdf":
            data = pdf_adapter.render(stmt)
            return Response(content=data, media_type="application/pdf")
        else:
            # JSON fallback
            return stmt
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
