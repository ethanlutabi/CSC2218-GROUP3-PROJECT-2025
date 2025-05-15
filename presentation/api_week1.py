# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from infrastructure.account_repo import InMemoryAccountRepository
# from infrastructure.transaction_repo import InMemoryTransactionRepository
# from application.services import AccountCreationService
# from application.services import TransactionService

# # Request schemas
# class CreateAccountRequest(BaseModel):
#     account_type: str
#     account_id: str
#     owner: str
#     initial_deposit: float = 0.0

# class TransactionRequest(BaseModel):
#     amount: float

# # FastAPI app initialization
# app = FastAPI()





# # Infrastructure -> Application wiring
# account_repo = InMemoryAccountRepository()
# transaction_repo = InMemoryTransactionRepository()
# account_service = AccountCreationService(account_repo)
# transaction_service = TransactionService(account_repo, transaction_repo)



# # Presentation Layer Endpoints
# @app.post("/accounts")
# def create_account(req: CreateAccountRequest):
#     try:
#         account_id = account_service.create_account(
#             req.account_type, req.account_id, req.owner, req.initial_deposit
#         )
#         return {"account_id": account_id}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.post("/accounts/{account_id}/deposit")
# def deposit(account_id: str, req: TransactionRequest):
#     try:
#         tx_id = transaction_service.deposit(account_id, req.amount)
#         return {"transaction_id": tx_id}
#     except (ValueError, KeyError) as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/accounts/{account_id}/withdraw")
# def withdraw(account_id: str, req: TransactionRequest):
#     try:
#         tx_id = transaction_service.withdraw(account_id, req.amount)
#         return {"transaction_id": tx_id}
#     except (ValueError, KeyError) as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @app.get("/accounts/{account_id}/balance")
# def get_balance(account_id: str):
#     try:
#         account = account_repo.get_account(account_id)
#         return {"balance": account.balance}
#     except KeyError as e:
#         raise HTTPException(status_code=404, detail=str(e))

# @app.get("/accounts/{account_id}/transactions")
# def get_transactions(account_id: str):
#     try:
#         txs = transaction_service.get_transactions(account_id)
#         return [
#             {
#                 "transaction_id": t.transaction_id,
#                 "type": t.transaction_type,
#                 "amount": t.amount,
#                 "timestamp": t.timestamp.isoformat(),
#             }
#             for t in txs
#         ]
#     except KeyError as e:
#         raise HTTPException(status_code=404, detail=str(e))

# @app.get("/", tags=["root"])
# def read_root():
#     return {"message": "Welcome to the Banking API. See /docs for usage."}



