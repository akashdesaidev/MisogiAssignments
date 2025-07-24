cart=[]

def add_cart(item) :
    cart.append(item)

def remove_last():
    cart.pop()

def remove(item):
    cart.removee(item)

def display_cart():
    print("Cart Items")
    for item in cart:
        print(cart.index(item),item)
    print()

while(True):
    print("1. Add to cart")
    print("2. Remove from cart")
    print("3. Display cart")
    print("4. Exit")
    choice =int(input())
    if choice == 1:
        item = input("Enter item to add: ")
        add_cart(item)
        display_cart()
    elif choice == 2:
        remove_last()
        display_cart()
    elif choice == 3:
        display_cart()
    elif choice == 4:
        break
    else:
        print("Invalid choice")

