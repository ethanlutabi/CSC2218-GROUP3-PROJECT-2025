<!-- this is the documentation including the python code with testing the uml class diagram FOR WEEK ONE-->


## 1. Domain Layer

### Account Class (`domain/account.py`)
```python
from dataclasses import dataclass
from enum import Enum, auto
from datetime import datetime
from typing import Optional

class AccountType(Enum):
    CHECKING = auto()
    SAVINGS = auto()

class AccountStatus(Enum):
    ACTIVE = auto()
    CLOSED = auto()

@dataclass
class Account:
    account_id: str
    account_type: AccountType
    balance: float
    status: AccountStatus
    creation_date: datetime
    owner_id: Optional[str] = None
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

### Transaction Class (`domain/transaction.py`)
```python
from dataclasses import dataclass
from enum import Enum, auto
from datetime import datetime

class TransactionType(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()

@dataclass
class Transaction:
    transaction_id: str
    transaction_type: TransactionType
    amount: float
    timestamp: datetime
    account_id: str
```

### Domain Tests (`tests/domain/test_account.py`)
```python
import unittest
from datetime import datetime
from domain.account import Account, AccountType, AccountStatus

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(
            account_id="123",
            account_type=AccountType.CHECKING,
            balance=100.0,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
    
    def test_deposit(self):
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150.0)
    
    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70.0)
    
    def test_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200)
```

## 2. Application Layer

### AccountCreationService (`application/account_creation_service.py`)
```python
from uuid import uuid4
from datetime import datetime
from domain.account import Account, AccountType, AccountStatus

class AccountCreationService:
    def __init__(self, account_repository):
        self.account_repository = account_repository
    
    def create_account(self, account_type: AccountType, initial_deposit: float = 0.0) -> str:
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        
        if account_type == AccountType.SAVINGS and initial_deposit < 100:
            raise ValueError("Savings accounts require minimum $100 deposit")
            
        account_id = str(uuid4())
        new_account = Account(
            account_id=account_id,
            account_type=account_type,
            balance=initial_deposit,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
        
        self.account_repository.save(new_account)
        return account_id
```

### TransactionService (`application/transaction_service.py`)
```python
from uuid import uuid4
from datetime import datetime
from domain.transaction import Transaction, TransactionType

class TransactionService:
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
    
    def deposit(self, account_id: str, amount: float) -> Transaction:
        account = self.account_repository.find_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        account.deposit(amount)
        self.account_repository.save(account)
        
        transaction = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            timestamp=datetime.now(),
            account_id=account_id
        )
        
        self.transaction_repository.save(transaction)
        return transaction
    
    def withdraw(self, account_id: str, amount: float) -> Transaction:
        account = self.account_repository.find_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        account.withdraw(amount)
        self.account_repository.save(account)
        
        transaction = Transaction(
            transaction_id=str(uuid4()),
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
            timestamp=datetime.now(),
            account_id=account_id
        )
        
        self.transaction_repository.save(transaction)
        return transaction
```

## 3. Infrastructure Layer

### AccountRepository (`infrastructure/account_repository.py`)
```python
from typing import Dict, Optional
from domain.account import Account

class InMemoryAccountRepository:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
    
    def save(self, account: Account) -> None:
        self.accounts[account.account_id] = account
    
    def find_by_id(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)
```

### TransactionRepository (`infrastructure/transaction_repository.py`)
```python
from typing import Dict, List, Optional
from domain.transaction import Transaction

class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.account_transactions: Dict[str, List[str]] = {}
    
    def save(self, transaction: Transaction) -> None:
        self.transactions[transaction.transaction_id] = transaction
        
        if transaction.account_id not in self.account_transactions:
            self.account_transactions[transaction.account_id] = []
        self.account_transactions[transaction.account_id].append(transaction.transaction_id)
    
    def find_by_account(self, account_id: str) -> List[Transaction]:
        if account_id not in self.account_transactions:
            return []
        
        return [
            self.transactions[tx_id] 
            for tx_id in self.account_transactions[account_id]
        ]
```

## 4. Presentation Layer (FastAPI)

### API Endpoints (`presentation/api.py`)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

from domain.account import AccountType as DomainAccountType
from application.account_creation_service import AccountCreationService
from application.transaction_service import TransactionService
from infrastructure.account_repository import InMemoryAccountRepository
from infrastructure.transaction_repository import InMemoryTransactionRepository

app = FastAPI()

# Setup dependencies
account_repo = InMemoryAccountRepository()
transaction_repo = InMemoryTransactionRepository()
account_creator = AccountCreationService(account_repo)
transaction_service = TransactionService(account_repo, transaction_repo)

# Request/Response Models
class AccountType(str, Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

class CreateAccountRequest(BaseModel):
    account_type: AccountType
    initial_deposit: float = 0.0

class TransactionRequest(BaseModel):
    amount: float

@app.post("/accounts", status_code=201)
def create_account(request: CreateAccountRequest):
    try:
        domain_type = DomainAccountType[request.account_type.value]
        account_id = account_creator.create_account(domain_type, request.initial_deposit)
        return {"account_id": account_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, request: TransactionRequest):
    try:
        transaction = transaction_service.deposit(account_id, request.amount)
        return {"transaction_id": transaction.transaction_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, request: TransactionRequest):
    try:
        transaction = transaction_service.withdraw(account_id, request.amount)
        return {"transaction_id": transaction.transaction_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    account = account_repo.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": account.balance, "available_balance": account.balance}

@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: str):
    transactions = transaction_repo.find_by_account(account_id)
    return transactions
```

## 5. Documentation

### UML Class Diagram
```
+----------------+       +-----------------+       +------------------+
|    Account     |       |   Transaction   |       | AccountCreation  |
+----------------+       +-----------------+       |     Service      |
| - account_id   |       | - transaction_id|       +------------------+
| - account_type |       | - type          |       | +create_account()|
| - balance      |       | - amount        |       +------------------+
| - status       |       | - timestamp     |
| - creation_date|       | - account_id    |       +------------------+
+----------------+       +-----------------+       |  Transaction     |
| +deposit()     |                                |     Service      |
| +withdraw()    |                                +------------------+
+----------------+                                | +deposit()       |
                                                  | +withdraw()      |
+----------------+       +-----------------+      +------------------+
| AccountRepo    |       | TransactionRepo |
+----------------+       +-----------------+
| +save()        |       | +save()         |
| +find_by_id()  |       | +find_by_acc()  |
+----------------+       +-----------------+
```

### Architecture Explanation
1. **Domain Layer**:
   - Contains core business logic (Account, Transaction)
   - No dependencies on other layers
   - Enforces business rules (min balance, valid transactions)

2. **Application Layer**:
   - Orchestrates domain objects
   - Depends only on domain layer
   - Handles use cases (account creation, transactions)

3. **Infrastructure Layer**:
   - Implements persistence (in-memory repos)
   - Could be replaced with database implementations
   - Handles technical details

4. **Presentation Layer**:
   - FastAPI endpoints
   - Converts between HTTP and application layer
   - Handles serialization/deserialization

## 6. Verification

### Manual Testing with Curl
```bash
# Create account
curl -X POST "http://localhost:8000/accounts" \
-H "Content-Type: application/json" \
-d '{"account_type":"CHECKING","initial_deposit":100}'

# Deposit
curl -X POST "http://localhost:8000/accounts/{account_id}/deposit" \
-H "Content-Type: application/json" \
-d '{"amount":50}'

# Withdraw
curl -X POST "http://localhost:8000/accounts/{account_id}/withdraw" \
-H "Content-Type: application/json" \
-d '{"amount":20}'

# Check balance
curl "http://localhost:8000/accounts/{account_id}/balance"

# View transactions
curl "http://localhost:8000/accounts/{account_id}/transactions"
```

### Automated Tests AND THE TEST RESULTS



<!-- import sys
import os
from fastapi.testclient import TestClient
import json
import unittest

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import your app
from presentation.api import app

class TestBankingAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        cls.client = TestClient(app)
        # Create test account to be used by all tests
        response = cls.client.post(
            "/accounts",
            json={"account_type": "CHECKING", "initial_deposit": 100}
        )
        cls.account_id = response.json()["account_id"]
    
    def setUp(self):
        """Run before each test"""
        self.client = self.__class__.client
        self.account_id = self.__class__.account_id
    
    def test_1_create_account(self):
        # Test checking account creation
        response = self.client.post(
            "/accounts",
            json={"account_type": "CHECKING", "initial_deposit": 100}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("account_id", data)
        self.assertEqual(data["account_type"], "CHECKING")
        self.assertEqual(data["balance"], 100.0)
        self.assertEqual(data["status"], "ACTIVE")
        self.assertIn("creation_date", data)
        
        # Test savings account creation
        response = self.client.post(
            "/accounts",
            json={"account_type": "SAVINGS", "initial_deposit": 200}
        )
        self.assertEqual(response.status_code, 201)
    
    def test_2_invalid_account_creation(self):
        # Test invalid account type
        response = self.client.post(
            "/accounts",
            json={"account_type": "INVALID", "initial_deposit": 100}
        )
        self.assertEqual(response.status_code, 422)
        
        # Test negative initial deposit
        response = self.client.post(
            "/accounts",
            json={"account_type": "CHECKING", "initial_deposit": -50}
        )
        self.assertEqual(response.status_code, 400)
        
        # Test insufficient savings account deposit
        response = self.client.post(
            "/accounts",
            json={"account_type": "SAVINGS", "initial_deposit": 50}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_3_deposit(self):            
        # Test valid deposit
        response = self.client.post(
            f"/accounts/{self.account_id}/deposit",
            json={"amount": 50}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["amount"], 50.0)
        
        # Test invalid deposit amounts
        response = self.client.post(
            f"/accounts/{self.account_id}/deposit",
            json={"amount": -10}
        )
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post(
            f"/accounts/{self.account_id}/deposit",
            json={"amount": 0}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_4_withdraw(self):
        # Test valid withdrawal
        response = self.client.post(
            f"/accounts/{self.account_id}/withdraw",
            json={"amount": 20}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["amount"], 20.0)
        
        # Test invalid withdrawals
        response = self.client.post(
            f"/accounts/{self.account_id}/withdraw",
            json={"amount": -10}
        )
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post(
            f"/accounts/{self.account_id}/withdraw",
            json={"amount": 0}
        )
        self.assertEqual(response.status_code, 400)
        
        # Test insufficient funds
        response = self.client.post(
            f"/accounts/{self.account_id}/withdraw",
            json={"amount": 1000}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_5_get_balance(self):
        response = self.client.get(f"/accounts/{self.account_id}/balance")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("balance", data)
        self.assertIn("available_balance", data)
    
    def test_6_get_transactions(self):
        response = self.client.get(f"/accounts/{self.account_id}/transactions")
        self.assertEqual(response.status_code, 200)
        transactions = response.json()
        self.assertIsInstance(transactions, list)

if __name__ == "__main__":
    unittest.main() -->



Run the test suite with:
```bash
python -m pytest tests/ -v


PS C:\Users\APUOL A.M\Desktop\group3> python -m pytest testing/test.py -v
================================================================= test session starts =================================================================
platform win32 -- Python 3.12.6, pytest-8.3.4, pluggy-1.5.0 -- C:\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\APUOL A.M\Desktop\group3
plugins: anyio-4.9.0
collected 6 items                                                                                                                                      

testing/test.py::TestBankingAPI::test_1_create_account PASSED                                                                                    [ 16%]
testing/test.py::TestBankingAPI::test_2_invalid_account_creation PASSED                                                                          [ 33%]
testing/test.py::TestBankingAPI::test_3_deposit SKIPPED (No account created)                                                                     [ 50%]
testing/test.py::TestBankingAPI::test_4_withdraw SKIPPED (No account created)                                                                    [ 66%]
testing/test.py::TestBankingAPI::test_5_get_balance SKIPPED (No account created)                                                                 [ 83%]
testing/test.py::TestBankingAPI::test_6_get_transactions SKIPPED (No account created)                                                            [100%] 

============================================================ 2 passed, 4 skipped in 1.48s ============================================================= 
PS C:\Users\APUOL A.M\Desktop\group3> python -m pytest testing/test.py -v
================================================================= test session starts =================================================================
platform win32 -- Python 3.12.6, pytest-8.3.4, pluggy-1.5.0 -- C:\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\APUOL A.M\Desktop\group3
plugins: anyio-4.9.0
collected 6 items                                                                                                                                      

testing/test.py::TestBankingAPI::test_1_create_account PASSED                                                                                    [ 16%]
testing/test.py::TestBankingAPI::test_2_invalid_account_creation PASSED                                                                          [ 33%]
testing/test.py::TestBankingAPI::test_3_deposit PASSED                                                                                           [ 50%]
testing/test.py::TestBankingAPI::test_4_withdraw PASSED                                                                                          [ 66%]
testing/test.py::TestBankingAPI::test_5_get_balance PASSED                                                                                       [ 83%] 
testing/test.py::TestBankingAPI::test_6_get_transactions PASSED                                                                                  [100%]

================================================================== 6 passed in 1.38s ================================================================== 
PS C:\Users\APUOL A.M\Desktop\group3> 




##this is prompt testing results
=== 🏦 Banking API Interactive Tester ===
Current Account: 5eca71e3-7e75-4ba9-b4be-f6181cd0cd44
=======================================

Main Menu:
1. 📝 Create Account
2. 💰 Deposit Money
3. 🏧 Withdraw Money
4. 📊 Check Balance
5. 📜 View Transactions
6. 🔄 Switch Account
7. 🚪 Exit

Select option (1-7):

📝 Create New Account
-------------------
Account type (1-CHECKING, 2-SAVINGS): 2
Initial deposit amount: $8000000

✅ Account created successfully!
Account ID: 14015e86-7fcc-4f4f-9779-a44fa14eb74c
Type: SAVINGS
Balance: $8000000.00

Press Enter to continue...

🏧 Make Withdrawal
-----------------
Amount to withdraw: $2000

✅ Withdrawal successful!
Amount: $2000.00

Press Enter to continue...


=== 🏦 Banking API Interactive Tester ===
Current Account: 14015e86-7fcc-4f4f-9779-a44fa14eb74c
=======================================

📊 Account Balance
-----------------
Current Balance: $7998000.00
Available Balance: $7998000.00

Press Enter to continue...

=== 🏦 Banking API Interactive Tester ===
Current Account: 14015e86-7fcc-4f4f-9779-a44fa14eb74c
=======================================

📜 Transaction History
---------------------

Date: 2025-04-19T04:15:12.614698
Type: WITHDRAW
Amount: $2000.00
ID: afb41c92-6c03-4e5b-b42e-c1a6704a5369

Press Enter to continue...

=== 🏦 Banking API Interactive Tester ===
Current Account: 14015e86-7fcc-4f4f-9779-a44fa14eb74c
=======================================

💰 Make Deposit
--------------
Amount to deposit: $7689959505

✅ Deposit successful!
Amount: $7689959505.00

Press Enter to continue...

=== 🏦 Banking API Interactive Tester ===
Current Account: 14015e86-7fcc-4f4f-9779-a44fa14eb74c
=======================================

📊 Account Balance
-----------------
Current Balance: $7697957505.00
Available Balance: $7697957505.00

Press Enter to continue...

```

## Success Criteria Met
1. Core account features implemented
2. Clean separation of concerns
3. Easy to add new account types
4. Expandable transaction types
5. Test coverage for critical paths
6. Documentation provided

The application is now ready for Week 2 features (transfers, notifications).












## WEEK TWO DELIVERY

7.1 Updated UML Diagram
+----------------+       +------------------+       +-------------------+
|   Transaction  |       | FundTransfer     |       | Notification      |
+----------------+       |     Service      |       |     Service       |
| +TRANSFER type |       +------------------+       +-------------------+
| +dest_account  |       | +transfer_funds()|       | +notify_transaction()
+----------------+       +------------------+       +-------------------+
                                                           ^
+----------------+       +------------------+              |
|  Account       |       | Transaction      |       +-------------------+
+----------------+       |     Logger       |       | Notification      |
| +can_transfer()|       +------------------+       |     Adapter       |
+----------------+       | +log_transaction()|      +-------------------+
                         +------------------+       | +send()          |
                                                    +-------------------+
7.2 Sequence Diagram for Transfer
User -> API: POST /transfers {source, dest, amount}
API -> FundTransferService: transfer_funds()
FundTransferService -> AccountRepo: get both accounts
FundTransferService -> SourceAccount: withdraw(amount)
FundTransferService -> DestAccount: deposit(amount)
FundTransferService -> TransactionRepo: save transfer
FundTransferService -> NotificationService: notify()
NotificationService -> Adapters: send notifications
API -> User: return transaction ID
Implementation Notes
Atomic Transfers: The FundTransferService ensures both withdrawal and deposit succeed or fail together

Decoupled Notifications: Notification service uses adapters pattern for different channels

Non-Invasive Logging: Decorator pattern adds logging without modifying core logic

Thread Safety: Repository locks prevent concurrent modification issues

Extensible Design: New notification adapters can be added without service changes

All Week 2 requirements have been implemented including:

Fund transfers between accounts

Automatic transaction notifications

Comprehensive transaction logging

New API endpoints

Updated domain models

Complete test coverage

System documentation

The implementation maintains clean architecture principles with:

Business logic in domain layer

Use cases in application layer

Technical details in infrastructure layer

Delivery mechanisms in presentation layer






## testing of results of week 2
<!-- import sys
import os
from datetime import datetime
from unittest.mock import MagicMock
from unittest import TestCase

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.fund_transfer_services import FundTransferService
from domain.account import Account, AccountType, AccountStatus
from domain.transaction import TransactionType

class TestFundTransferService(TestCase):
    def setUp(self):
        self.mock_account_repo = MagicMock()
        self.mock_transaction_repo = MagicMock()
        self.service = FundTransferService(self.mock_account_repo, self.mock_transaction_repo)
        
        # Create test accounts with all required parameters
        self.source = Account(
            account_id="acc1",
            account_type=AccountType.CHECKING,
            balance=100.0,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
        self.dest = Account(
            account_id="acc2",
            account_type=AccountType.SAVINGS,
            balance=50.0,
            status=AccountStatus.ACTIVE,
            creation_date=datetime.now()
        )
        
        # Configure mock to return our test accounts
        self.mock_account_repo.find_by_id.side_effect = lambda x: (
            self.source if x == "acc1" else (self.dest if x == "acc2" else None)
        )

    def test_successful_transfer(self):
        """Test that funds are transferred correctly between accounts"""
        # Perform transfer
        transaction = self.service.transfer_funds("acc1", "acc2", 30.0)
        
        # Verify balances were updated
        self.assertEqual(self.source.balance, 70.0)
        self.assertEqual(self.dest.balance, 80.0)
        
        # Verify transaction record was created
        self.assertEqual(transaction.transaction_type, TransactionType.TRANSFER)
        self.assertEqual(transaction.amount, 30.0)
        self.assertEqual(transaction.account_id, "acc1")
        self.assertEqual(transaction.destination_account_id, "acc2")
        
        # Verify repositories were called
        self.mock_account_repo.find_by_id.assert_any_call("acc1")
        self.mock_account_repo.find_by_id.assert_any_call("acc2")
        self.mock_account_repo.save.assert_any_call(self.source)
        self.mock_account_repo.save.assert_any_call(self.dest)
        self.mock_transaction_repo.save.assert_called_once()

    def test_transfer_to_same_account(self):
        """Test that transferring to the same account fails"""
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc1", 30.0)

    def test_insufficient_funds(self):
        """Test that transfer fails with insufficient funds"""
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc2", 150.0)

    def test_inactive_source_account(self):
        """Test that transfer fails if source account is inactive"""
        self.source.status = AccountStatus.CLOSED
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc2", 30.0)

    def test_inactive_destination_account(self):
        """Test that transfer fails if destination account is inactive"""
        self.dest.status = AccountStatus.CLOSED
        with self.assertRaises(ValueError):
            self.service.transfer_funds("acc1", "acc2", 30.0) -->


PS C:\Users\APUOL A.M\Desktop\group3> python -m pytest testing/test2.py -v
================================================================= test session starts =================================================================
platform win32 -- Python 3.12.6, pytest-8.3.4, pluggy-1.5.0 -- C:\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\APUOL A.M\Desktop\group3
plugins: anyio-4.9.0
collected 5 items                                                                                                                                      

testing/test2.py::TestFundTransferService::test_inactive_destination_account PASSED                                                              [ 20%]
testing/test2.py::TestFundTransferService::test_inactive_source_account PASSED                                                                   [ 40%]
testing/test2.py::TestFundTransferService::test_insufficient_funds PASSED                                                                        [ 60%]
testing/test2.py::TestFundTransferService::test_successful_transfer PASSED                                                                       [ 80%]
testing/test2.py::TestFundTransferService::test_transfer_to_same_account PASSED                                                                  [100%] 

================================================================== 5 passed in 0.30s ================================================================== 
PS C:\Users\APUOL A.M\Desktop\group3> 


## prompt testing results
=== 🏦 Banking API Interactive Tester ===
Current Account: 3dcf892b-09b4-45fe-bb56-d0953ad6a3df
=======================================

Main Menu:
1. 📝 Create Account
2. 💰 Deposit Money
3. 🏧 Withdraw Money
4. 🔄 Transfer Funds
5. 📊 Check Balance
6. 📜 View Transactions
7. 🔔 Notification Preferences
8. 🔄 Switch Account
9. 🚪 Exit


=== 🏦 Banking API Interactive Tester ===
Current Account: 3dcf892b-09b4-45fe-bb56-d0953ad6a3df
=======================================

💰 Make Deposit
--------------
Amount to deposit: $5000

✅ Deposit successful!
Amount: $5000.00

Press Enter to continue...


=== 🏦 Banking API Interactive Tester ===
Current Account: 3dcf892b-09b4-45fe-bb56-d0953ad6a3df
=======================================

🏧 Make Withdrawal
-----------------
Amount to withdraw: $100

✅ Withdrawal successful!
Amount: $100.00

Press Enter to continue...

## Testing transfer and the notification

Available accounts:
1. f46aa319-fde2-4788-a661-ef54b2c83654 (CHECKING) - $400.00

Select destination account (number): 1
Amount to transfer: $500
Email to user123: Transfer of $500.00 from account 3dcf892b-09b4-45fe-bb56-d0953ad6a3df to f46aa319-fde2-4788-a661-ef54b2c83654
SMS to user123: Transfer of $500.00 from account 3dcf892b-09b4-45fe-bb56-d0953ad6a3df to f46aa319-fde2-4788-a661-ef54b2c83654

✅ Transfer successful!
Transferred $500.00 to account f46aa319-fde2-4788-a661-ef54b2c83654

Press Enter to continue...

=== 🏦 Banking API Interactive Tester ===
Current Account: 3dcf892b-09b4-45fe-bb56-d0953ad6a3df
=======================================

🔔 Notification Preferences
-------------------------

Notification Types:
1. Email notifications
2. SMS notifications

Select notification type (1-2): 1

Select notification type (1-2): 1
Enable notifications? (y/n): y

❌ Failed to update preferences: {"account_id":"3dcf892b-09b4-45fe-bb56-d0953ad6a3df","notify_type":"email","enabled":true,"message":"Notification preference updated"}

Press Enter to continue...

