
from functools import reduce

evenSquare=[i*i for i in range(1,11) if i%2==0]
print(evenSquare)

Captilalize = list(map(str.capitalize, ['hello', 'world',"check"]))
print(Captilalize)

result  = reduce(lambda a,b: a+b ,evenSquare)
print(result) 

