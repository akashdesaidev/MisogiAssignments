from collections import defaultdict
students=["Alice","Bob","Carol","David","Eve"]
scores=[85,92,78,88,95]
# Create a Numbered List of Students

# Print each student’s name with a number starting from 1 (e.g., 1. Alice).

# Pair Students with Their Scores Using enumerate()

# Combine both lists to display each student's name alongside their score.
numbered_list=list(enumerate(students,start=1))
for number,name in numbered_list:
    print(number,name)
print(numbered_list)

# Map Positions to Student Names

# Create a dictionary where keys are positions (starting from 0) and values are the student names.
position_map=defaultdict(str)
for number,name in numbered_list:
    position_map[number]=name
print(position_map)    

for i in range(len(scores)):
    if scores[i]>90:
        print(i+1)