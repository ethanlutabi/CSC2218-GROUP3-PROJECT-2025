# # THIS IS WEEK TWO SEPARATE CODE
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from infrastructure.account_repo import InMemoryAccountRepository
# from infrastructure.transaction_repo import InMemoryTransactionRepository

# from infrastructure.adapters.notify import ConsoleNotificationAdapter
# from application.services import AccountCreationService, TransactionService
# from application.transfer_logging.transfer_service import FundTransferService
# from infrastructure.adapters.logging import TransactionServiceLogger, ConsoleLogger


# # Pydantic schemas
# class CreateAccountRequest(BaseModel):
#     account_type: str
#     account_id: str
#     owner: str
#     initial_deposit: float = 0.0

# class TransactionRequest(BaseModel):
#     amount: float

# class TransferRequest(BaseModel):
#     source_account_id: str
#     destination_account_id: str
#     amount: float

# # Initialize app
# app = FastAPI()

# # Root endpoint
# @app.get("/", include_in_schema=False)
# def root():
#     return {"message": "Welcome! See /docs for API endpoints."}


# # Infrastructure wiring
# account_repo = InMemoryAccountRepository()
# transaction_repo = InMemoryTransactionRepository()
# notifier = ConsoleNotificationAdapter()
# logger = ConsoleLogger()

# # Application services
# account_service = AccountCreationService(account_repo)
# base_tx_service = TransactionService(account_repo, transaction_repo)
# tx_service_with_logging = TransactionServiceLogger(base_tx_service, logger)
# fund_transfer_service = FundTransferService(account_repo, transaction_repo, notification_adapter=notifier)




# # Presentation endpoints
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
#         tx_id = tx_service_with_logging.deposit(account_id, req.amount)
#         return {"transaction_id": tx_id}
#     except (ValueError, KeyError) as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/accounts/{account_id}/withdraw")
# def withdraw(account_id: str, req: TransactionRequest):
#     try:
#         tx_id = tx_service_with_logging.withdraw(account_id, req.amount)
#         return {"transaction_id": tx_id}
#     except (ValueError, KeyError) as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/accounts/transfer")
# def transfer(req: TransferRequest):
#     try:
#         tx_id = fund_transfer_service.transfer_funds(
#             req.source_account_id, req.destination_account_id, req.amount
#         )
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
#         txs = base_tx_service.get_transactions(account_id)
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

# @app.get("/transactions/{tx_id}")
# def get_transaction(tx_id: str):
#     try:
#         tx = transaction_repo.find_transaction(tx_id)
#         return {
#             "transaction_id": tx.transaction_id,
#             "type": tx.transaction_type,
#             "amount": tx.amount,
#             "account_id": tx.account_id,
#             "timestamp": tx.timestamp.isoformat(),
#         }
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Transaction not found")

# @app.get("/transactions/{tx_id}")
# def get_transaction(tx_id: str):
#     try:
#         tx = tx_service_with_logging.get_transaction(tx_id)
#         return {
#             "transaction_id": tx.transaction_id,
#             "type": tx.transaction_type,
#             "amount": tx.amount,
#             "account_id": tx.account_id,
#             "timestamp": tx.timestamp.isoformat(),
#         }
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Transaction not found")


