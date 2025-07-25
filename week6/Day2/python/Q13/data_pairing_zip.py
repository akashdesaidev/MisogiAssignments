from collections import defaultdict
print("Create Product-Price Pairs")

# Use zip() to pair each product with its corresponding price.

products = ['apple', 'banana', 'cherry','mango']
prices = [299.99, 250.50, 999.0,25.50]
quantities=[5,20,15,8]
product_price_pairs = list(zip(products, prices))

print(product_price_pairs)
print()


# Calculate Total Value for Each Product

# For each product, calculate the total inventory value using the formula: price × quantity.


# Create a dictionary where each product maps to another dictionary containing its price and quantity.
print("Build a Product Catalog Dictionary")
dictionary=defaultdict(lambda: {'price':0,'quantities':0,'total_value':0})
for i in range(len(products)) :
    dictionary[products[i]]={'price':prices[i],'quantities':quantities[i],'total_value':quantities[i]*prices[i]}
print(dict(dictionary))
print()


# Identify and print the names of products with a quantity less than 10.
print("Low Stock Products")
for item in dictionary:
    if dictionary[item]['quantities']<10:
        print(item)