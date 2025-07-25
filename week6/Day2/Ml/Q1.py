def add_vectors(a, b):
    return [x + y for x, y in zip(a, b)]

def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def are_orthogonal(a, b):
    return dot_product(a, b) == 0
# Sample input
a = [1, 2, 3]
b = [4, 5, 6]
# print(list(zip(a,b)))

# Output
print("Sum:", add_vectors(a, b))
print("Dot Product:", dot_product(a, b))
print("Orthogonal:", are_orthogonal(a, b))
