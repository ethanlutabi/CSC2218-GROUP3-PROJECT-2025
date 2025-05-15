import pytest
from fastapi.testclient import TestClient
from presentation.api import app

client = TestClient(app)

def test_full_account_lifecycle():
    # Create account
    create_payload = {
        "account_type": "checking",
        "account_id": "intacc1",
        "owner": "Integration User",
        "initial_deposit": 1000.0
    }
    response = client.post("/accounts", json=create_payload)
    assert response.status_code == 201
    account_id = response.json().get("account_id")
    assert account_id == "intacc1"

    # Deposit
    deposit_payload = {"amount": 500.0}
    response = client.post(f"/accounts/{account_id}/deposit", json=deposit_payload)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

    # Withdraw
    withdraw_payload = {"amount": 200.0}
    response = client.post(f"/accounts/{account_id}/withdraw", json=withdraw_payload)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

    # Get balance
    response = client.get(f"/accounts/{account_id}/balance")
    assert response.status_code == 200
    balance = response.json().get("balance")
    assert balance == 1300.0  # 1000 + 500 - 200

    # List transactions
    response = client.get(f"/accounts/{account_id}/transactions")
    assert response.status_code == 200
    transactions = response.json()
    assert isinstance(transactions, list)
    assert len(transactions) >= 2

    # Transfer funds to another account
    # Create destination account
    dest_payload = {
        "account_type": "checking",
        "account_id": "intacc2",
        "owner": "Integration User 2",
        "initial_deposit": 500.0
    }
    response = client.post("/accounts", json=dest_payload)
    assert response.status_code == 201

    transfer_payload = {
        "source_account_id": account_id,
        "destination_account_id": "intacc2",
        "amount": 300.0
    }
    response = client.post("/accounts/transfer", json=transfer_payload)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

    # Check balances after transfer
    response = client.get(f"/accounts/{account_id}/balance")
    assert response.status_code == 200
    assert response.json().get("balance") == 1000.0  # 1300 - 300

    response = client.get("/accounts/intacc2/balance")
    assert response.status_code == 200
    assert response.json().get("balance") == 800.0  # 500 + 300

    # Calculate interest
    interest_payload = {"calculationDate": "2023-01-01"}
    response = client.post(f"/accounts/{account_id}/interest/calculate", json=interest_payload)
    assert response.status_code == 200
    assert "interest" in response.json()

    # Preview interest
    response = client.post(f"/accounts/{account_id}/interest/preview", json=interest_payload)
    assert response.status_code == 200
    assert "interest" in response.json()

    # Configure limits
    limits_payload = {"dailyLimit": 1000.0, "monthlyLimit": 5000.0}
    response = client.patch(f"/accounts/{account_id}/limits", json=limits_payload)
    assert response.status_code == 200

    # Get limits
    response = client.get(f"/accounts/{account_id}/limits")
    assert response.status_code == 200
    limits = response.json()
    assert "dailyLimit" in limits and "monthlyLimit" in limits

    # Get statement JSON
    # Add a deposit transaction for statement month
    client.post(f"/accounts/{account_id}/deposit", json={"amount": 100.0})
    response = client.get(f"/accounts/{account_id}/statement?year=2023&month=1&format=json")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    # Get statement CSV
    response = client.get(f"/accounts/{account_id}/statement?year=2023&month=1&format=csv")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert content_type.startswith("text/csv")

    # Get statement PDF
    response = client.get(f"/accounts/{account_id}/statement?year=2023&month=1&format=pdf")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert content_type == "application/pdf"
