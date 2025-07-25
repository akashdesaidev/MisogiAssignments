grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]
print(grades[2:7])
print(list(filter(lambda x:  x>85,grades)))
grades[3]=95
print(grades)
grades.append(10)
grades.append(10)
grades.append(10)
print(grades)
print(sorted(grades,reverse=True)[0:6])