from abc import ABC,abstractmethod
class BankAccount(ABC):
    total_accounts = 5
    bank_name = "bank"

    def __init__(self):
        self.set_total_accounts()  # Increase total accounts on each new account

    @classmethod
    def set_total_accounts(cls):
        BankAccount.total_accounts += 1

    def get_total_account(self):
        return BankAccount.total_accounts


class Account(BankAccount):
    def __init__(self, id, name, balance):
        super().__init__()
        self.account_id = id
        self.name = name
        self._balance = balance  # internal storage

    @property
    def balance(self):
        """Getter for balance"""
        return self._balance

    @balance.setter
    def balance(self, value):
        """Setter for balance (with validation)"""
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def deposit(self, amount):
        """Deposit using balance setter"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance = self.balance + amount  # 👈 calls the setter
        return True

    def withdraw(self, amount):
        """Withdraw using balance setter"""
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance = self.balance - amount  # 👈 calls the setter
        return True
     
    @abstractmethod
    def calculate_monthly_interest():
        pass


class savings_Account(Account):
    min_balance=100
    def __init__(self,id,name,balance) -> None:
        super().__init__(id,name,balance)
        if balance<self.min_balance:
            raise ValueError(f"min balance require {self.min_balance} to create account")
       
    def calculate_monthly_interest(self):
        # Example: 4% annual interest
        return round((self.balance * 0.04)/12, 2)
    
class checking_Account(Account):
    min_balance=1000
    def __init__(self,id,name,balance) -> None:
        super().__init__(id,name,balance)
        if balance<self.min_balance:
            raise ValueError(f"min balance require {self.min_balance} to create account")
    def calculate_monthly_interest(self):
        # Example: 1.5% annual interest
        return round((self.balance * 0.015)/12, 2) 


savings_account =savings_Account(1,"john",200)
checking_account =checking_Account(1,"john",1500)
print(savings_account.balance)
print(checking_account.balance)
print(BankAccount.total_accounts)

savings_account.withdraw(50)
print(savings_account.balance)
savings_account.deposit(150)
print(savings_account.balance)
print(savings_account.calculate_monthly_interest())

try:
    invalid_account= savings_Account(1,"akas",-100)
except Exception as e:
    print(e)