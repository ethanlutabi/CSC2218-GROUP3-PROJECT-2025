import requests
import time

API_BASE_URL = "http://localhost:8000"

def create_account(account_id: str, owner: str, initial_deposit: float):
    url = f"{API_BASE_URL}/accounts"
    payload = {
        "account_type": "checking",
        "account_id": account_id,
        "owner": owner,
        "initial_deposit": initial_deposit
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print(f"Account {account_id} created successfully.")
        return True
    else:
        print(f"Failed to create account: {response.status_code} - {response.text}")
        return False

def save_pdf_statement(account_id: str, year: int, month: int, filename: str):
    url = f"{API_BASE_URL}/accounts/{account_id}/statement"
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
    account_id = "intacc1"
    owner = "Integration User"
    initial_deposit = 1000.0

    if create_account(account_id, owner, initial_deposit):
        # Wait a moment to ensure account creation is processed
        time.sleep(1)
        save_pdf_statement(account_id, 2023, 1, "statement_jan_2023.pdf")
