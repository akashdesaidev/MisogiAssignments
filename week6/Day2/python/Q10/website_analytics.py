monday_visitors={"user1","user2","user3","user4","user5"}
tuesday_visitors = {"user1","user2", "user4","user6","user7","user8"}  
wednesday_visitors = {"user1", "user3","user6", "user9","user10"} 

# Unique Visitors Across All Days
print("Find the total number of unique visitors who visited on any of the three days.")
print(len(set(monday_visitors|tuesday_visitors|wednesday_visitors)))
print()
# Returning Visitors on Tuesday
print("Identify users who visited on both Monday and Tuesday.")
print(monday_visitors & tuesday_visitors)
print()

# New Visitors Each Day
# Determine which users visited for the first time each day (i.e., not seen on previous days).
print("users visited for the first time each day")
print(tuesday_visitors - monday_visitors)
print(wednesday_visitors-tuesday_visitors-monday_visitors)
print()
# Loyal Visitors
print("Find users who visited the site on all three days.")
print(monday_visitors& tuesday_visitors&wednesday_visitors)
print()
# Daily Visitor Overlap Analysis
# Compare and print overlaps between each pair of days (e.g., Monday-Tuesday, Tuesday-Wednesday, etc.)
print("Overlap monday-tuesday")
print(monday_visitors & tuesday_visitors)
print("Overlap tuesday-wednesday")
print(wednesday_visitors & tuesday_visitors)