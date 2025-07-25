fruits_list=["apple","banana","cherry","date","elderberry"]
fruits_tuple=("apple","banana","cherry","date","elderberry")
fruits_set={"apple","banana","cherry","date","elderberry"}
fruits_dict={"apple":5,"banana":3,"cherry":8,"date":4,"elderberry":5}

print("apple" in fruits_list)
print("apple" in fruits_tuple)
print("apple" in fruits_set)
print("apple" in fruits_dict)

print(len(fruits_list),len(fruits_set),len(fruits_dict),len(fruits_tuple))
print()
print("List")
for item in fruits_list:
    print(item)
print()
print("Tuple")    
for item in fruits_tuple:
    print(item)    
print()
print("set")
for item in fruits_set:
    print(item)
print()    

print("Dictonary")
for key in fruits_dict:
    print(key)