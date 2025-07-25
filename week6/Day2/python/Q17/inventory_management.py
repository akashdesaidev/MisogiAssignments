inventory={
    "apples":{"price":1.5,"quantity":100},
    "bananas":{"price":0.75,"quantity":105},
    "oranges":{"price":2.00,"quantity":80}
}

def add_item():
    print("Enter name of product: ")
    name=input()
    print("Enter price of product: ")
    price=float(input())
    print("Enter quantity of item: ")
    quantity=int(input())
    inventory[name]={"price":price,"quantity":quantity}
    print(inventory)

# add_item()    
def update_product():
    print("Enter name of product you want to  update: ")
    name=input()
    print("Enter updated price: ")
    new_price=float(input())
    inventory[name]["price"]=new_price
    print(inventory)

# update_product()    
def sell():
     print("Enter name of product you want to  sell: ")
     name=input()
     print("Enter quantity ")
     qty=int(input())
     inventory[name]["quantity"]-=qty
     print(inventory)

# sell() 
def calcualate_total():
    sum=0
    for value in inventory.values():
        sum+=value["price"]*value["quantity"]
    print(sum)
# calcualate_total()