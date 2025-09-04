# q1
# 1. Given two vectors of length `n`, find the **dot product** between them.   
#     **Input**: Two lists of numbers  
#     **Output**: A single number (dot product)
# dot product = x1*y1 + x2*y2 + x3*y3 + ...
l1=[1,2,3,4,5]
l2=[6,7,8,9,10]

def dot_product(l1,l2):
    ans=[]
    for i in range(len(l1)):
        ans.append(l1[i]*l2[i])
    return ans

print("dot product:",dot_product(l1,l2))

# q2
# 2. Given two vectors of length `n`, find the **Euclidean distance** between them.    
#     **Input**: Two lists of numbers   
#     **Output**: A single number (distance)
# euclidean distance = sqrt((x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2 + ...)
q1=[1,2,3,4,5]
q2=[6,7,8,9,10]

def euclidean_distance(q1,q2):
    ans=0
    for i in range(len(q1)):
        ans+=((q1[i]-q2[i])**2)
    return ans**0.5

print("euclidean distance:",euclidean_distance(q1,q2))

# q3
# 3. Given two vectors of length `n`, find the **Manhattan distance** between them.
#     **Input**: Two lists of numbers  
#     **Output**: A single number (distance)
# manhattan distance = |x1-x2| + |y1-y2| + |z1-z2| + ...
q1=[1,2,3,4,5]
q2=[6,7,8,9,10]

def manhattan_distance(q1,q2):
    ans=0
    for i in range(len(q1)):
        ans+=abs(q1[i]-q2[i])
    return ans

print("manhattan distance:",manhattan_distance(q1,q2))

# q4
# 4. Given two vectors, compute the **cosine similarity** between them.   
#     **Input**: Two lists of numbers   
#     **Output**: A float representing similarity
# cosine similarity = (x1*y1 + x2*y2 + x3*y3 + ...) / (sqrt(x1^2 + x2^2 + x3^2 + ...) * sqrt(y1^2 + y2^2 + y3^2 + ...))
# cosine_similarity = (A · B) / (||A|| * ||B||)
# Where:
#   A · B = sum of products of corresponding elements of A and B
#   ||A|| = sqrt(sum of squares of elements of A)
#   ||B|| = sqrt(sum of squares of elements of B)

q1 = [1, 2, 3, 4, 5]
q2 = [6, 7, 8, 9, 10]

def cosine_similarity(q1, q2):
    dot = 0
    norm1 = 0
    norm2 = 0
    for i in range(len(q1)):
        dot += q1[i] * q2[i]
        norm1 += q1[i] ** 2
        norm2 += q2[i] ** 2
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / ((norm1 ** 0.5) * (norm2 ** 0.5))

print("cosine similarity:",cosine_similarity(l1, l2))

# q5
# 5. Given two matrices of size `m x n` and `n x p`, compute their **matrix multiplication**.   
#     **Input**: Two 2D lists   
#     **Output**: A 2D list

l1 = [[1, 2, 3],
      [4, 5, 6],
      [7, 8, 9]]

l2 = [[1, 2, 3],
      [4, 5, 6],
      [7, 8, 9]]

def matrix_multiplication(l1, l2):
    m = len(l1)
    n = len(l1[0])
    p = len(l2[0])
    # Initialize result matrix with zeros
    ans = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                ans[i][j] += l1[i][k] * l2[k][j]
    return ans

print("matrix multiplication:", matrix_multiplication(l1, l2))

# 6. Given a matrix of size `m x n`, compute its **transpose**.  
#     **Input**: A 2D list   
#     **Output**: A 2D list (transposed)

l1=[[1,2,3],
    [4,5,6],
    [7,8,9]]

def transpose(l1):
    ans=[]
    for i in range(len(l1[0])):
        ans.append([])
        for j in range(len(l1)):
            ans[i].append(l1[j][i])
    return ans

print("transpose:",transpose(l1))


# 7. Given a matrix, compute its **trace** (sum of diagonal elements).
#     **Input**: A square 2D list  
#     **Output**: A single number

input=[[1,2,3],
       [3,4,3],
       [2,3,6]]
def trace(input):
    i=0
    j=0
    ans=0
    while i<len(input) and j<len(input[0]):
        ans+=input[i][j]
        i+=1
        j+=1
    return ans        
print("sum of  diagonnal",trace(input))

# 8. Given a square matrix, compute its **determinant** (2x2 or 3x3 only).   
#     **Input**: A 2D list  
#     **Output**: A single number


def determinant(matrix):
    n = len(matrix)
    # 2x2 matrix
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    # 3x3 matrix
    elif n == 3:
        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[0][2]
        d = matrix[1][0]
        e = matrix[1][1]
        f = matrix[1][2]
        g = matrix[2][0]
        h = matrix[2][1]
        i = matrix[2][2]
        return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
    else:
        raise ValueError("Only 2x2 or 3x3 matrices are supported.")

# Example usage:
mat2 = [[1,2],
        [3,4]]
mat3 = [[1,2,3],
        [4,5,6],
        [7,8,9]]
print("determinant 2x2:", determinant(mat2))
print("determinant 3x3:", determinant(mat3))



# 9. Given a square matrix, check whether it's **symmetric**.  
#     **Input**: A 2D list   
#     **Output**: Boolean value

input=[[1,2,3],
       [2,4,3],
       [4,3,6]]
input2=[
       [1,2,3],
       [2,4,3],
       [3,3,6]]

def Sym(input):
    symetric=True
    for  i in range(len(input)):
        for j in range(len(input[0])):
            if  input[i][j] != input[j][i]:
                symetric=False
    return symetric
print("symetric",Sym(input))
print("symetric",Sym(input2))

# 10. Given a square matrix, check whether it's **identity matrix**.   
#     **Input**: A 2D list
#     **Output**: Boolean value

input=[[1,2,3],
       [2,4,3],
       [4,3,6]]
# this is the identiy matrix so result will be true
input2=[[1,0,0],
        [0,1,0],
        [0,0,1]]
def identity_matrix(input):   
    for i in range(len(input)):
        for j in range(len(input[0])):
            if i==j:
                 if input[i][j]!=1:
                     return False
            else:
               if input[i][j]!=0:
                return False
    return True

print("identity Matrix",identity_matrix(input))
print("identity Matrix",identity_matrix(input2))