# # presentation layer (FastAPI)



# from datetime import date
# from fastapi import APIRouter, HTTPException, FastAPI
# from pydantic import BaseModel
# from fastapi.responses import Response

# router = APIRouter()
# app = FastAPI()
# # request schemas for week3
# class InterestRequest(BaseModel):
#     calculationDate: date

# class LimitConfig(BaseModel):
#     dailyLimit: float
#     monthlyLimit: float

# @router.post("/accounts/{account_id}/interest/calculate")
# def calculate_interest(account_id: str, req: InterestRequest):
#     try:
#         interest = interest_service.apply_interest_to_account(account_id, req.calculationDate)
#         return {"interest": interest}
#     except Exception as e:
#         raise HTTPException(400, str(e))

# @router.patch("/accounts/{account_id}/limits")
# def update_limits(account_id: str, cfg: LimitConfig):
#     limit_service.configure_limits(account_id, cfg.dailyLimit, cfg.monthlyLimit)
#     return {"dailyUsed": limit_service.get_limits(account_id).daily_used,
#             "monthlyUsed": limit_service.get_limits(account_id).monthly_used}

# @router.get("/accounts/{account_id}/limits")
# def get_limits(account_id: str):
#     limits = limit_service.get_limits(account_id)
#     return {"dailyLimit": limits.daily_limit, "monthlyLimit": limits.monthly_limit,
#             "dailyUsed": limits.daily_used, "monthlyUsed": limits.monthly_used}

# @router.get("/accounts/{account_id}/statement")
# def get_statement(account_id: str, year: int, month: int, format: str = 'json'):
#     try:
#         data = statement_service.generate_statement(account_id, year, month, date.today(), fmt=format)
#         if format == 'csv':
#             return Response(content=data, media_type='text/csv')
#         return Response(content=data, media_type='application/json')
#     except Exception as e:
#         raise HTTPException(400, str(e))

# # wiring for week3
# from infrastructure.account_repo import InMemoryAccountRepository
# from infrastructure.transaction_repo import InMemoryTransactionRepository
# from infrastructure.interest.interest_service import (
#     InterestServiceImpl,
#     LimitEnforcementServiceImpl,
#     StatementServiceImpl
# )

# # instantiate
# account_repo = InMemoryAccountRepository()
# transaction_repo = InMemoryTransactionRepository()

# interest_service = InterestServiceImpl(account_repo)
# limit_service = LimitEnforcementServiceImpl(account_repo)
# statement_service = StatementServiceImpl(account_repo, transaction_repo)

