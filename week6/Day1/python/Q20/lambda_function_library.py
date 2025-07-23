from functools import reduce
square= lambda x:x*x
factorial =lambda x :1 if x == 0 else x * factorial(x - 1)
reverse=lambda x:x[::-1]
uppercase=lambda x:x.upper()
sum_of_list=lambda a:reduce(lambda x,y:x+y,a)
filter_evens=lambda a: list(filter(lambda x:x%2==0,a))

print(square(3))
print(factorial(3))
print(reverse([5,6,7]))
print(uppercase("hello"))
print(sum_of_list([1,2,3]))
print(filter_evens([1,2,3,4,5,6]))