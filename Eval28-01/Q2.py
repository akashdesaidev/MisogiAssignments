class InsufficientFundsError(ValueError):
    pass



class User():
    def __init__(self,bank):
     self.name:str
     self.bank=bank

    def withdraw(self,amount):
      print(self.bank.balance)
      if amount>self.bank.balance:
         raise InsufficientFundsError
      else:
         bank.balance -=amount 
         print(f"{amount} withdraw succesfully")
       
         



class Bank():
    def __init__(self):
        self.balance=1000

bank= Bank()
user1=  User(bank)

amount=[700,600]

for i in amount:
   try:  
      user1.withdraw(i)
   except Exception as e:
        print("Insufficient funds",e)
