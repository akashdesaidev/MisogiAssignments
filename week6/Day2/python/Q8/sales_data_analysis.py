sales_data=[("Q1",[("Jan",1000),("Feb",1200),("Mar",1100)]),
            ("Q2",[("Apr",1300),("May",1250),("Jun",1400)]),
            ("Q3",[("Jul",1350),("Aug",1450),("Sep",1300)])]


# Use unpacking to compute and display the total sales for each quarter.
for Q,data in sales_data:
    sum=0
    for month,sale in data:
        sum+=sale
    print(Q,sum)  

 # Identify the month with the highest individual sales across all quarters.  

highest_sale_month=sales_data[0][1][0][1]
highest_sale_month_amount=sales_data[0][1][0][1]
for Q,data in sales_data:
    sum=0
    for month,amount in data:
        #    print(highest_sale_month_amount)
           if amount > highest_sale_month_amount:
                highest_sale_month  =month
                highest_sale_month_amount=amount
print(highest_sale_month)

# Generate a flat list of all monthly sales in the format: ("Jan", 1000), ("Feb", 1200), ....
flat=[]

for Q,data in sales_data:
     for item in data:
          flat.append(item)

print(flat)          
     
    #  Use tuple unpacking while iterating to clearly separate months, sales values, and quarters.
    # already done