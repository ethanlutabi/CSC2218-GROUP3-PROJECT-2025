import requests

def save_pdf_statement(account_id: str, year: int, month: int, filename: str):
    url = f"http://localhost:8000/accounts/{account_id}/statement"
    params = {
        "year": year,
        "month": month,
        "format": "pdf"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"PDF statement saved to {filename}")
    else:
        print(f"Failed to get PDF statement: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Example usage with existing account
    save_pdf_statement("intacc1", 2023, 1, "statement_jan_2023.pdf")
