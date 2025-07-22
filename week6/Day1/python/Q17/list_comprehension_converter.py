squares=[i*i for i in range(10)]
evens = [i for i in range(10) if i%2==0]
pairs=[(x,y) for x in range(3) for y in range(2)] 
print(squares)
print(evens)
print(pairs)