import time
def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = list(func(*args, **kwargs))  # consume generator fully
        end = time.time()
        print(f"Execution Time: {end - start:.6f} seconds")
        return result
    return wrapper


@measure_time
def prime_generator(limit):
    """Generate prime numbers up to a given limit.""" 
    for num in range(2, limit + 1):
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                break
        else:
            # print(prime, end=" ")
            yield num  


# Example usage:
for prime in prime_generator(200000):
   print(prime, end=" ")
   pass
    
