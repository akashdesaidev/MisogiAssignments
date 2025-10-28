

class Product():

    def __init__(self,name,price,quanity):
        self.name=name
        self.price=price
        self.quantity=quanity

    def __str__(self):
        return f"name={self.name} price={self.price} qunatiy={self.quantity}" 

    def __lt__(self,item1):
        return self.price<item1.price


class Inventory():
    def __init__(self): 
        self.items=[]

    def add_product(self,product):
        self.items.append(product)

    def __getitem__():
        pass

    def __len__(self):
        ans = len(self.items)
        return   ans  
pr1 = Product("pr1",200,4)
pr2 = Product("p2",400,4)

print(pr1.__lt__(pr2)) 

Inv = Inventory()
print(Inv.__len__())
Inv.add_product(pr1) 
Inv.add_product(pr2) 
print(Inv.__len__())


print(pr1)
