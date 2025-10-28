from typing import DefaultDict
students = [
    {"name": "Alice", "marks": [80, 75, 90]},
    {"name": "Bob", "marks": [70, 60, 65]},
    {"name": "Charlie", "marks": [95, 85, 100]},
    {"name": "David", "marks": [60, 70, 80]}
]

grade={
    "A": [],
    "B":[],
    "C":[]
}


for i in students:
    sum=0
    for j in i["marks"]:
        print(j)
        sum+=j
    avg = sum/len(i["marks"])

    if avg>=85:
        grade["A"].append(i["name"])    
    elif (avg>=70 and avg< 85) :
        grade["B"].append(i["name"])    
    else:
        grade["C"].append(i["name"])    


print(grade)