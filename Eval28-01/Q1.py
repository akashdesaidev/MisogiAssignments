from time import time_ns
start = 1
end = 1000000

def measure_time(func):
    st = time_ns()
    def exec_fn(self,*args,**kwargs):
        func(*args,**kwargs)
    en = time_ns()-st
    print(en)  
    return exec_fn 

@measure_time
def normal_sum(start,end):    
    sum= 0
    for i in range(start,end):
        sum+=i**2  
    return sum    

print(normal_sum(start,end))    

