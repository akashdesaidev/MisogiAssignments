import time
import threading
start = 1
end = 1000000

def measure_time(func):
    """Decorator to measure execution time of a function."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"\nExecution Time: {end - start:.6f} seconds")
        return result
    return wrapper


def sum(start,end):    
    sum= 0
    for i in range(start,end):
        sum+=i**2  
    return sum    

@measure_time
def normal():
    sum(start,end)  
    sum(start,end)  

@measure_time
def threaded():
    t1 = threading.Thread(target=sum, args=(start, end))
    t2 = threading.Thread(target=sum, args=(start, end))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

normal()
threaded()
# threaded one laos took same time ot execute even with the threading becuase  of the python GIL which keep switching between both the execution