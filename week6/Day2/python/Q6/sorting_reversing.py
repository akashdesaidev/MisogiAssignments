employees=[("Alice",50000,"Engieenering"),("Alice",45000,"Engieenering"),("BOB",60000,"Marketing"),("Carol",55000,"Sales")]
sort_asc_salary=sorted(employees,key=lambda x:x[1])
sort_des_salary=sorted(employees,key=lambda x:x[1])[::-1]
sort_dep_salary=sorted(employees,key=lambda x:(x[2],x[1]))
rev = employees[::-1]

print(employees)
print(sort_asc_salary)
print(sort_des_salary)
print(sort_dep_salary)
print(rev)  