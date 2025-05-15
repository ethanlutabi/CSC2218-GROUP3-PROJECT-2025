# infrastructure/week3/pdf_statement_adapter.py
from io import BytesIO
from domain.interest.statement import MonthlyStatement

class PdfStatementAdapter:
    """
    Adapter to export a MonthlyStatement to PDF format using ReportLab.
    """
    def __init__(self):
        try:
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
            from reportlab.lib.styles import getSampleStyleSheet
            self.SimpleDocTemplate = SimpleDocTemplate
            self.Paragraph = Paragraph
            self.Spacer = Spacer
            self.Table = Table
            self.getSampleStyleSheet = getSampleStyleSheet
            self.pdf_enabled = True
        except ImportError:
            self.pdf_enabled = False

    def render(self, statement: MonthlyStatement) -> bytes:
        if not self.pdf_enabled:
            raise RuntimeError("ReportLab is required for PDF generation.")

        buffer = BytesIO()
        doc = self.SimpleDocTemplate(buffer)
        styles = self.getSampleStyleSheet()
        elements = []

        # Title
        elements.append(self.Paragraph(f"Monthly Statement: {statement.month}/{statement.year}", styles['Title']))
        elements.append(self.Spacer(1, 12))

        # Summary table
        summary_data = [
            ['Account ID', statement.account_id],
            ['Opening Balance', f"{statement.opening_balance:.2f}"],
            ['Closing Balance', f"{statement.closing_balance:.2f}"],
            ['Interest Earned', f"{statement.interest_earned:.2f}"],
            ['Generated On', statement.generated_on.isoformat()]
        ]
        elements.append(self.Table(summary_data))
        elements.append(self.Spacer(1, 24))

        # Transactions table
        tx_header = ['Tx ID', 'Type', 'Amount', 'Timestamp']
        tx_rows = [
            [tx.transaction_id, tx.transaction_type, f"{tx.amount:.2f}", tx.timestamp.isoformat()]
            for tx in statement.transactions
        ]
        elements.append(self.Paragraph("Transactions", styles['Heading2']))
        elements.append(self.Table([tx_header] + tx_rows))

        doc.build(elements)
        return buffer.getvalue()
