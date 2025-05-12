import csv
import io
from typing import Dict, List, Optional, Union, BinaryIO
from datetime import datetime
from domain.transaction import Transaction

class InMemoryTransactionRepository:
    # Existing methods...
    
    # Added for statement generation
    def generate_statement(self, account_id: str, start_date: datetime, 
                          end_date: datetime, format_type: str = "csv") -> Union[str, bytes]:
       
        transactions = self.list_transactions(account_id)
        
        # Filter by date range
        filtered_transactions = [
            tx for tx in transactions 
            if start_date <= tx.timestamp <= end_date
        ]
        
        if format_type.lower() == "csv":
            return self._generate_csv_statement(filtered_transactions)
        elif format_type.lower() == "pdf":
            return self._generate_pdf_statement(filtered_transactions, account_id)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_csv_statement(self, transactions: List[Transaction]) -> str:
        """Generate a CSV statement from transactions."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["Transaction ID", "Date", "Type", "Amount", "Description"])
        
        # Write transactions
        for tx in transactions:
            writer.writerow([
                tx.transaction_id,
                tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                tx.transaction_type,
                tx.amount,
                tx.description
            ])
        
        return output.getvalue()
    
    def _generate_pdf_statement(self, transactions: List[Transaction], account_id: str) -> bytes:
       
        # Mock PDF generation - in a real implementation, use ReportLab
        pdf_content = f"PDF Statement for account {account_id}\n\n"
        
        for tx in transactions:
            pdf_content += (
                f"ID: {tx.transaction_id}, "
                f"Date: {tx.timestamp.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Type: {tx.transaction_type}, "
                f"Amount: {tx.amount}, "
                f"Description: {tx.description}\n"
            )
        
        # In a real implementation, this would return PDF bytes
        return pdf_content.encode('utf-8')
