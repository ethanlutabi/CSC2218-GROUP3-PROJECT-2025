from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from domain.entities.account import Account
from domain.entities.transaction import Transaction
from application.services.account_creation_service import AccountCreationService
from application.services.transaction_service import TransactionService
from application.dtos import (
    CreateAccountDTO,
    TransactionDTO,
    AccountBalanceDTO,
    TransactionHistoryDTO
)
from infrastructure.repositories.account_repository import AccountRepository
from infrastructure.repositories.transaction_repository import TransactionRepository

router = APIRouter(prefix="/accounts", tags=["accounts"])

# Initialize repositories and services
account_repo = AccountRepository()
transaction_repo = TransactionRepository()
account_creation_service = AccountCreationService(account_repo)
transaction_service = TransactionService(account_repo, transaction_repo)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(account_dto: CreateAccountDTO):
    """Endpoint to create a new account"""
    try:
        account_id = account_creation_service.create_account(account_dto)
        return {"account_id": account_id, "message": "Account created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{account_id}/deposit")
def deposit_funds(account_id: str, transaction_dto: TransactionDTO):
    """Endpoint to deposit funds into an account"""
    try:
        transaction = transaction_service.deposit(account_id, transaction_dto.amount)
        account = account_repo.get_by_id(account_id)
        return {
            "transaction_id": transaction.transaction_id,
            "new_balance": account.balance,
            "available_balance": account.available_balance
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{account_id}/withdraw")
def withdraw_funds(account_id: str, transaction_dto: TransactionDTO):
    """Endpoint to withdraw funds from an account"""
    try:
        transaction = transaction_service.withdraw(account_id, transaction_dto.amount)
        account = account_repo.get_by_id(account_id)
        return {
            "transaction_id": transaction.transaction_id,
            "new_balance": account.balance,
            "available_balance": account.available_balance
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{account_id}/balance")
def get_account_balance(account_id: str):
    """Endpoint to get account balance"""
    account = account_repo.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return {
        "balance": account.balance,
        "available_balance": account.available_balance
    }

@router.get("/{account_id}/transactions")
def get_transaction_history(account_id: str):
    """Endpoint to get transaction history for an account"""
    transactions = transaction_repo.get_for_account(account_id)
    if not transactions:
        # Check if account exists
        if not account_repo.get_by_id(account_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
    return {"transactions": transactions}
