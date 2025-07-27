from collections import defaultdict
class Product:
    all_prodcuts=[]
    products_category=defaultdict(int)
    def __init__(self,product_id,name,price,category,stock_quantity) -> None:
        self.product_id=product_id
        self.name=name    
        self.price=price
        self.category=category
        self.stock_quantiy=stock_quantity
        Product.all_prodcuts.append(self)
        Product.products_category[category]+=1
    
    def get_product_info(self):
        return f"{self.name} {self.price} {self.category}"
    
    def get_total_products():
        return len(Product.all_prodcuts)
    
    def order(self,qty):
        if qty<self.stock_quantiy:
            self.stock_quantiy-=qty
            return True
        else:
            raise(ValueError("Insufficeint stock"))
        

class Customer:
    def __init__(self,customer_id,name,email,customer_type) -> None:
        self.customer_id=customer_id
        self.name=name    
        self.email=email
        self.discount_rate=10 if customer_type=="Premium" else 0
        self.customer_type=customer_type
        self.orders=defaultdict(int)

    def get_discount_rate(self):
        return self.discount_rate
    
    def purchased(self,product,qty):
        self.orders[product]+=qty

class ShoppingCart:     
    def __init__(self,customer) -> None:
        self.customer=customer
        self.items=defaultdict(int) 

    def add_item(self,product,qty):
        self.items[product]=qty

    def get_total_items(self):
        return sum(self.items.values())
    
    def get_sub_total(self):
        return sum( value*key.price for key,value in self.items.items())

    def get_total(self):
        print(self.customer.__dict__)
        return self.get_sub_total()-(self.get_sub_total()*self.customer.discount_rate/100) 
    
    def palce_order(self):
        for item,qty in self.items.items():
            try:
                item.order(qty)
                self.customer.purchased(item,qty)

            except Exception as e:
                print(e)    
        return True

laptop=Product("P001","Gaming Laptop",20000,"Electronics",10)        
book=Product("P003","Python Programming",250,"Books",12)        
shirt=Product("P003","Cotton Shirt",200,"Clothes",50)      

print(laptop.get_product_info())
print(book.get_product_info())
print(shirt.get_product_info())
print(Product.get_total_products())

customer=Customer("C101","akash","akash@email.com","Premium")
print(customer.get_discount_rate())

cart = ShoppingCart(customer)

cart.add_item(shirt,1)
cart.add_item(laptop,2)
print(cart.get_total_items())
print(cart.get_sub_total())
print(cart.get_total())

print(laptop.stock_quantiy)
print(cart.palce_order())
print(laptop.stock_quantiy)
print(customer.orders)