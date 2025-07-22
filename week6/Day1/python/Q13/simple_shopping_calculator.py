ItemPrice1=int(input("Enter the price of item 1: "))
Quantity1=int(input("Enter the quantity of item 1: "))  
ItemPrice2=int(input("Enter the price of item 2: "))
Quantity2=int(input("Enter the quantity of item 2: "))
ItemPrice3=int(input("Enter the price of item 3: "))
Quantity3=int(input("Enter the quantity of item 3: "))
subTotal=ItemPrice1*Quantity1+ItemPrice2*Quantity2+ItemPrice3*Quantity3
print("Item1:",Quantity1,"x",ItemPrice1,"=" ,ItemPrice1*Quantity1)
print("Item2:",Quantity2,"x",ItemPrice2,"=" ,ItemPrice2*Quantity2)
print("Item3:",Quantity3,"x",ItemPrice3,"=" ,ItemPrice3*Quantity3)
print("subTotal:",subTotal)
print("Tax (8.5%):",format((subTotal*0.085),".2f"))
print("Total:",format((subTotal+subTotal*0.085),".2f"))




