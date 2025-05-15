from datetime import date
from application.interest.statement_service import StatementServiceInterface
from domain.interest.statement import MonthlyStatement

from infrastructure.interest.pdf_statement_adapter import PdfStatementAdapter
from infrastructure.interest.csv_statement_adapter import CsvStatementAdapter

class StatementServiceImpl(StatementServiceInterface):
    def __init__(self, account_repo, transaction_repo):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def generate_statement(self, account_id: str, year: int, month: int, as_of: date) -> MonthlyStatement:
        account = self.account_repo.get_account(account_id)
        all_txs = self.transaction_repo.list_transactions(account_id)

        # Filter transactions for the month
        txs = [t for t in all_txs if t.timestamp.year == year and t.timestamp.month == month]

        closing_balance = account.balance

        # Estimate opening balance by reversing transactions
        opening_balance = closing_balance
        for t in txs:
            if t.transaction_type == "DEPOSIT":
                opening_balance -= t.amount
            else:
                opening_balance += t.amount

        interest_earned = sum(t.amount for t in txs if t.transaction_type == "INTEREST")

        return MonthlyStatement(
            account_id=account_id,
            year=year,
            month=month,
            opening_balance=opening_balance,
            closing_balance=closing_balance,
            interest_earned=interest_earned,
            transactions=txs,
            generated_on=as_of
        )
