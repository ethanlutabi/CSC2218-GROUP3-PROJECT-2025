import pytest
from fastapi.testclient import TestClient
from presentation.api import app
from datetime import datetime

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Banking API. See /docs for usage."}

def test_create_account():
    payload = {
        "account_type": "checking",
        "account_id": "testacc1",
        "owner": "Test User",
        "initial_deposit": 1000.0
    }
    response = client.post("/accounts", json=payload)
    assert response.status_code == 201
    assert "account_id" in response.json()

def test_deposit_and_withdraw():
    # Create account first
    payload = {
        "account_type": "checking",
        "account_id": "testacc2",
        "owner": "Test User",
        "initial_deposit": 0.0
    }
    client.post("/accounts", json=payload)

    deposit_payload = {"amount": 500.0}
    response = client.post("/accounts/testacc2/deposit", json=deposit_payload)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

    withdraw_payload = {"amount": 200.0}
    response = client.post("/accounts/testacc2/withdraw", json=withdraw_payload)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

def test_get_balance():
    payload = {
        "account_type": "checking",
        "account_id": "testacc3",
        "owner": "Test User",
        "initial_deposit": 1000.0
    }
    client.post("/accounts", json=payload)

    response = client.get("/accounts/testacc3/balance")
    assert response.status_code == 200
    assert "balance" in response.json()

def test_list_transactions():
    payload = {
        "account_type": "checking",
        "account_id": "testacc4",
        "owner": "Test User",
        "initial_deposit": 0.0
    }
    client.post("/accounts", json=payload)

    deposit_payload = {"amount": 100.0}
    client.post("/accounts/testacc4/deposit", json=deposit_payload)

    response = client.get("/accounts/testacc4/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_transfer():
    # Create source and destination accounts
    client.post("/accounts", json={"account_type": "checking", "account_id": "srcacc", "owner": "Src", "initial_deposit": 1000})
    client.post("/accounts", json={"account_type": "checking", "account_id": "destacc", "owner": "Dest", "initial_deposit": 500})

    transfer_payload = {
        "source_account_id": "srcacc",
        "destination_account_id": "destacc",
        "amount": 200.0
    }
    response = client.post("/accounts/transfer", json=transfer_payload)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

def test_calculate_and_preview_interest():
    client.post("/accounts", json={"account_type": "checking", "account_id": "intacc", "owner": "Int", "initial_deposit": 1000})

    interest_payload = {"calculationDate": "2023-01-01"}
    response = client.post("/accounts/intacc/interest/calculate", json=interest_payload)
    assert response.status_code == 200
    assert "interest" in response.json()

    response = client.post("/accounts/intacc/interest/preview", json=interest_payload)
    assert response.status_code == 200
    assert "interest" in response.json()

def test_configure_and_get_limits():
    client.post("/accounts", json={"account_type": "checking", "account_id": "limacc", "owner": "Lim", "initial_deposit": 1000})

    limits_payload = {"dailyLimit": 1000.0, "monthlyLimit": 5000.0}
    response = client.patch("/accounts/limacc/limits", json=limits_payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert "dailyLimit" in json_resp
    assert "monthlyLimit" in json_resp

    response = client.get("/accounts/limacc/limits")
    assert response.status_code == 200
    json_resp = response.json()
    assert "dailyLimit" in json_resp
    assert "monthlyLimit" in json_resp

def test_get_statement_json():
    client.post("/accounts", json={"account_type": "checking", "account_id": "stmtacc", "owner": "Stmt", "initial_deposit": 1000})

    # Add a deposit transaction for the statement month
    deposit_payload = {"amount": 100.0}
    client.post("/accounts/stmtacc/deposit", json=deposit_payload)

    response = client.get("/accounts/stmtacc/statement?year=2023&month=1&format=json")
    assert response.status_code == 200
    # The response should be JSON serializable
    assert isinstance(response.json(), dict)

def test_get_statement_csv():
    client.post("/accounts", json={"account_type": "checking", "account_id": "stmtacc2", "owner": "Stmt2", "initial_deposit": 1000})

    deposit_payload = {"amount": 100.0}
    client.post("/accounts/stmtacc2/deposit", json=deposit_payload)

    response = client.get("/accounts/stmtacc2/statement?year=2023&month=1&format=csv")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert content_type.startswith("text/csv")


def test_get_statement_pdf():
    client.post("/accounts", json={"account_type": "checking", "account_id": "stmtacc3", "owner": "Stmt3", "initial_deposit": 1000})

    # Add a deposit transaction for the statement month
    deposit_payload = {"amount": 100.0}
    client.post("/accounts/stmtacc3/deposit", json=deposit_payload)

    response = client.get("/accounts/stmtacc3/statement?year=2023&month=1&format=pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
