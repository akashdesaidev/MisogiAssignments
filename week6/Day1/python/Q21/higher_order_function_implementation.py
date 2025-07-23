def custom_map(func,iterable):
    return [func(x) for x in iterable]

print(custom_map(lambda x: x+1 ,[1,2,3,4]))


def custom_Filter(func,iterable):
    return [item for item in iterable if func(item)]
print(custom_Filter(lambda x:x%2==0,[1,2,3,4,5,6]))

def custom_reduce(func,iterable):
    result=iterable[0]  
    for x in iterable[1:]:
        result=func(result,x)
    return result

print(custom_reduce(lambda x,y:x+y,[1,2,3,4,5]))