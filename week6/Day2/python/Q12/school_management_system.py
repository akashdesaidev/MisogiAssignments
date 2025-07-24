school={
    "Math":{
        "teacher":"Mr.Smith",
        "students":[("Alice",85),("bob",93),("Carol",78)]
    },
    "Science":{
        "teacher":"Ms.Johnson",
        "students":[("David",88),("Eve",94),("Frank",82)]
    }
}

# Print Teacher Names
print("Iterate through all classes and print the name of each teacher.")

for cls in school:
    print(school[cls]["teacher"])
print()
# Calculate Class Average Grades

print("For each class, calculate and display the average grade of the students.")

for cls in school:
    marks=0
    for student,grade in school[cls]["students"]:
        marks+=grade
    print(cls,marks/len(school[cls]["students"]))
print()


# Identify the student with the highest grade among all students across every class.
print("Find Top Student Across All Classes")
for cls in school:
    name, grade =school[cls]["students"][0]
    marks=grade
    top_student=name
    for student,grade in school[cls]["students"]:
        #  print(student,grade,marks,top_student)
         if grade>marks: 
             marks=grade
             top_student=student
    print(cls,"topper",top_student)
print()

# Use Unpacking

# Use tuple unpacking to extract and work with student names and grades separately.
# done in above examples