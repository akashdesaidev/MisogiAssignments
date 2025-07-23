# Identify and print the student who has the highest grade from the list.
students=[(101,"ALice",85,20),(102,"BOB",92,19),(103,"Carol",78,21),(104,"David",88,20)]

grade_sorted=sorted(students,key=lambda x:x[2],reverse=True)
print("HighestGrade student is: ",grade_sorted[0][1],"with grade",grade_sorted[0][2])

# Generate a new list containing only the name and grade of each student in the format: ("Alice", 85).
name_grade=[]

for Roll,name,grade,age in students:
    name_grade.append((name,grade))

print(name_grade)

# Attempt to change the grade of a student in the original list and show why this is not allowed with tuples. Explain briefly why tuples are preferred for immutable records like student data.
students[0][2]=32

# This error on terminal because tuples are immutable

# Traceback (most recent call last):
#   File "D:\Misogi\Assignments\week6\Day2\python\Q7\student_records.py", line 16, in <module>
#     students[0][2]=32
# TypeError: 'tuple' object does not support item assignment