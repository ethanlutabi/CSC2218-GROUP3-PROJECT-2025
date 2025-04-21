import sys
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
    unittest.main()