# infrastructure/week3/csv_statement_adapter.py
import csv
from io import StringIO
from domain.interest.statement import MonthlyStatement

class CsvStatementAdapter:
    """
    Adapter to export a MonthlyStatement to CSV format.
    """
    def render(self, statement: MonthlyStatement) -> bytes:
        buffer = StringIO()
        writer = csv.writer(buffer)
        # Summary header
        writer.writerow([
            'account_id', 'year', 'month',
            'opening_balance', 'closing_balance',
            'interest_earned', 'generated_on'
        ])
        writer.writerow([
            statement.account_id,
            statement.year,
            statement.month,
            statement.opening_balance,
            statement.closing_balance,
            statement.interest_earned,
            statement.generated_on.isoformat()
        ])
        writer.writerow([])

        # Transaction detail header
        writer.writerow(['transaction_id', 'transaction_type', 'amount', 'timestamp'])
        for tx in statement.transactions:
            writer.writerow([
                tx.transaction_id,
                tx.transaction_type,
                tx.amount,
                tx.timestamp.isoformat()
            ])
        return buffer.getvalue().encode('utf-8')