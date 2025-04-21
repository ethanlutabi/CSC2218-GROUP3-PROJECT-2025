# # testing/interactive_tester.py
# import sys
# import os
# from fastapi.testclient import TestClient


# # Add the parent directory to Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from presentation.api import app

# class InteractiveBankTester:
#     def __init__(self):
#         self.client = TestClient(app)
#         self.current_account = None
#         self.test_accounts = []
        
#     def clear_screen(self):
#         os.system('cls' if os.name == 'nt' else 'clear')
    
#     def display_header(self):
#         self.clear_screen()
#         print("=== 🏦 Banking API Interactive Tester ===")
#         if self.current_account:
#             print(f"Current Account: {self.current_account}")
#         print("=======================================")
    
#     def display_menu(self):
#         print("\nMain Menu:")
#         print("1. 📝 Create Account")
#         print("2. 💰 Deposit Money")
#         print("3. 🏧 Withdraw Money")
#         print("4. 📊 Check Balance")
#         print("5. 📜 View Transactions")
#         print("6. 🔄 Switch Account")
#         print("7. 🚪 Exit")
    
#     def create_account(self):
#         self.display_header()
#         print("\n📝 Create New Account")
#         print("-------------------")
        
#         while True:
#             account_type = input("Account type (1-CHECKING, 2-SAVINGS): ").strip()
#             if account_type == "1":
#                 account_type = "CHECKING"
#                 break
#             elif account_type == "2":
#                 account_type = "SAVINGS"
#                 break
#             else:
#                 print("Invalid choice. Please enter 1 or 2.")
        
#         while True:
#             try:
#                 amount = float(input("Initial deposit amount: $"))
#                 if amount >= 0:
#                     break
#                 print("Amount must be positive")
#             except ValueError:
#                 print("Please enter a valid number")
        
#         response = self.client.post(
#             "/accounts",
#             json={"account_type": account_type, "initial_deposit": amount}
#         )
        
#         if response.status_code == 201:
#             account = response.json()
#             self.test_accounts.append(account)
#             self.current_account = account["account_id"]
#             print("\n✅ Account created successfully!")
#             print(f"Account ID: {account['account_id']}")
#             print(f"Type: {account['account_type']}")
#             print(f"Balance: ${account['balance']:.2f}")
#         else:
#             print(f"\n❌ Failed to create account: {response.text}")
#         input("\nPress Enter to continue...")
    
#     def deposit(self):
#         if not self.current_account:
#             print("\n⚠️ Please create or select an account first!")
#             input("Press Enter to continue...")
#             return
        
#         self.display_header()
#         print("\n💰 Make Deposit")
#         print("--------------")
        
#         while True:
#             try:
#                 amount = float(input("Amount to deposit: $"))
#                 if amount > 0:
#                     break
#                 print("Amount must be positive")
#             except ValueError:
#                 print("Please enter a valid number")
        
#         response = self.client.post(
#             f"/accounts/{self.current_account}/deposit",
#             json={"amount": amount}
#         )
        
#         if response.status_code == 200:
#             print("\n✅ Deposit successful!")
#             print(f"Amount: ${amount:.2f}")
#         else:
#             print(f"\n❌ Deposit failed: {response.text}")
#         input("\nPress Enter to continue...")
    
#     def switch_account(self):
#         if not self.test_accounts:
#             print("\n⚠️ No accounts available. Please create one first.")
#             input("Press Enter to continue...")
#             return
            
#         self.display_header()
#         print("\n🔄 Switch Account")
#         print("----------------")
#         for i, account in enumerate(self.test_accounts, 1):
#             print(f"{i}. {account['account_id']} ({account['account_type']}) - ${account['balance']:.2f}")
        
#         while True:
#             try:
#                 choice = int(input("\nSelect account (number): "))
#                 if 1 <= choice <= len(self.test_accounts):
#                     self.current_account = self.test_accounts[choice-1]["account_id"]
#                     print(f"\n✅ Switched to account {self.current_account}")
#                     break
#                 print("Invalid selection")
#             except ValueError:
#                 print("Please enter a number")
#         input("\nPress Enter to continue...")
    
#     def run(self):
#         while True:
#             self.display_header()
#             self.display_menu()
            
#             choice = input("\nSelect option (1-7): ").strip()
            
#             if choice == "1":
#                 self.create_account()
#             elif choice == "2":
#                 self.deposit()
#             elif choice == "3":
#                 self.withdraw()
#             elif choice == "4":
#                 self.check_balance()
#             elif choice == "5":
#                 self.view_transactions()
#             elif choice == "6":
#                 self.switch_account()
#             elif choice == "7":
#                 print("\n👋 Thank you for using the Banking API Tester!")
#                 break
#             else:
#                 print("\n❌ Invalid choice. Please try again.")
#                 input("Press Enter to continue...")

# if __name__ == "__main__":
#     tester = InteractiveBankTester()
#     tester.run()

# testing/interactive_tester.py
import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from presentation.api import app

class InteractiveBankTester:
    def __init__(self):
        self.client = TestClient(app)
        self.current_account = None
        self.test_accounts = []
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        self.clear_screen()
        print("=== 🏦 Banking API Interactive Tester ===")
        if self.current_account:
            print(f"Current Account: {self.current_account}")
        print("=======================================")
    
    def display_menu(self):
        print("\nMain Menu:")
        print("1. 📝 Create Account")
        print("2. 💰 Deposit Money")
        print("3. 🏧 Withdraw Money")
        print("4. 📊 Check Balance")
        print("5. 📜 View Transactions")
        print("6. 🔄 Switch Account")
        print("7. 🚪 Exit")
    
    def create_account(self):
        self.display_header()
        print("\n📝 Create New Account")
        print("-------------------")
        
        while True:
            account_type = input("Account type (1-CHECKING, 2-SAVINGS): ").strip()
            if account_type == "1":
                account_type = "CHECKING"
                break
            elif account_type == "2":
                account_type = "SAVINGS"
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        
        while True:
            try:
                amount = float(input("Initial deposit amount: $"))
                if amount >= 0:
                    break
                print("Amount must be positive")
            except ValueError:
                print("Please enter a valid number")
        
        response = self.client.post(
            "/accounts",
            json={"account_type": account_type, "initial_deposit": amount}
        )
        
        if response.status_code == 201:
            account = response.json()
            self.test_accounts.append(account)
            self.current_account = account["account_id"]
            print("\n✅ Account created successfully!")
            print(f"Account ID: {account['account_id']}")
            print(f"Type: {account['account_type']}")
            print(f"Balance: ${account['balance']:.2f}")
        else:
            print(f"\n❌ Failed to create account: {response.text}")
        input("\nPress Enter to continue...")
    
    def deposit(self):
        if not self.current_account:
            print("\n⚠️ Please create or select an account first!")
            input("Press Enter to continue...")
            return
        
        self.display_header()
        print("\n💰 Make Deposit")
        print("--------------")
        
        while True:
            try:
                amount = float(input("Amount to deposit: $"))
                if amount > 0:
                    break
                print("Amount must be positive")
            except ValueError:
                print("Please enter a valid number")
        
        response = self.client.post(
            f"/accounts/{self.current_account}/deposit",
            json={"amount": amount}
        )
        
        if response.status_code == 200:
            print("\n✅ Deposit successful!")
            print(f"Amount: ${amount:.2f}")
        else:
            print(f"\n❌ Deposit failed: {response.text}")
        input("\nPress Enter to continue...")

    def withdraw(self):
        if not self.current_account:
            print("\n⚠️ Please create or select an account first!")
            input("Press Enter to continue...")
            return
        
        self.display_header()
        print("\n🏧 Make Withdrawal")
        print("-----------------")
        
        while True:
            try:
                amount = float(input("Amount to withdraw: $"))
                if amount > 0:
                    break
                print("Amount must be positive")
            except ValueError:
                print("Please enter a valid number")
        
        response = self.client.post(
            f"/accounts/{self.current_account}/withdraw",
            json={"amount": amount}
        )
        
        if response.status_code == 200:
            print("\n✅ Withdrawal successful!")
            print(f"Amount: ${amount:.2f}")
        else:
            print(f"\n❌ Withdrawal failed: {response.text}")
        input("\nPress Enter to continue...")

    def check_balance(self):
        if not self.current_account:
            print("\n⚠️ Please create or select an account first!")
            input("Press Enter to continue...")
            return
        
        self.display_header()
        print("\n📊 Account Balance")
        print("-----------------")
        
        response = self.client.get(f"/accounts/{self.current_account}/balance")
        
        if response.status_code == 200:
            balance = response.json()
            print(f"Current Balance: ${balance['balance']:.2f}")
            print(f"Available Balance: ${balance['available_balance']:.2f}")
        else:
            print(f"\n❌ Failed to get balance: {response.text}")
        input("\nPress Enter to continue...")

    def view_transactions(self):
        if not self.current_account:
            print("\n⚠️ Please create or select an account first!")
            input("Press Enter to continue...")
            return
        
        self.display_header()
        print("\n📜 Transaction History")
        print("---------------------")
        
        response = self.client.get(f"/accounts/{self.current_account}/transactions")
        
        if response.status_code == 200:
            transactions = response.json()
            if not transactions:
                print("No transactions found")
            else:
                for tx in transactions:
                    print(f"\nDate: {tx['timestamp']}")
                    print(f"Type: {tx['transaction_type']}")
                    print(f"Amount: ${tx['amount']:.2f}")
                    print(f"ID: {tx['transaction_id']}")
        else:
            print(f"\n❌ Failed to get transactions: {response.text}")
        input("\nPress Enter to continue...")

    def switch_account(self):
        if not self.test_accounts:
            print("\n⚠️ No accounts available. Please create one first.")
            input("Press Enter to continue...")
            return
            
        self.display_header()
        print("\n🔄 Switch Account")
        print("----------------")
        for i, account in enumerate(self.test_accounts, 1):
            print(f"{i}. {account['account_id']} ({account['account_type']}) - ${account['balance']:.2f}")
        
        while True:
            try:
                choice = int(input("\nSelect account (number): "))
                if 1 <= choice <= len(self.test_accounts):
                    self.current_account = self.test_accounts[choice-1]["account_id"]
                    print(f"\n✅ Switched to account {self.current_account}")
                    break
                print("Invalid selection")
            except ValueError:
                print("Please enter a number")
        input("\nPress Enter to continue...")

    def run(self):
        while True:
            self.display_header()
            self.display_menu()
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.check_balance()
            elif choice == "5":
                self.view_transactions()
            elif choice == "6":
                self.switch_account()
            elif choice == "7":
                print("\n👋 Thank you for using the Banking API Tester!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    tester = InteractiveBankTester()
    tester.run()