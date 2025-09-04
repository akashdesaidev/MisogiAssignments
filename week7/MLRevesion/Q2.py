import math
# **1.** Given a list of numbers, calculate the **mean**.
# **Input:** A list of numbers
# **Output:** A single number
def mean(l):
    return sum(l)/len(l)

print("mean:",mean([1,2,3,4,5]))

# **2.** Given a list of numbers, calculate the **median**.
# **Input:** A list of numbers
# **Output:** A single number
def median(l):
    l.sort()
    return l[len(l)//2]

print("median:",median([1,2,3,4,5]))

# **3.** Given a list of numbers, calculate the **mode**.

# **Input:** A list of numbers

# **Output:** A number or list of numbers

def mode(l):
    return max(set(l), key=l.count)

print("mode:",mode([1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]))

# **4.** Given a list of numbers, calculate the **variance**.
# **Input:** A list of numbers
# **Output:** A single number
def variance(l):
    return sum((x - mean(l)) ** 2 for x in l) / len(l)

print("variance:",variance([1,2,3,4,5]))

# **5.** Given a list of numbers, calculate the **standard deviation**.
# **Input:** A list of numbers
# **Output:** A single number
def standard_deviation(l):
    return variance(l) ** 0.5

print("standard deviation:",standard_deviation([1,2,3,4,5]))

# **6.** Given a list of class labels, calculate the **entropy**.
# **Input:** A list of categorical values
# **Output:** A float (entropy value)

# In statistics, machine learning, and information theory:
# Entropy measures uncertainty or disorder in a system.
# High entropy → very uncertain, lots of unpredictability
# Low entropy → more certain, less unpredictability

def entropy(l):
    return -sum(p * math.log2(p) for p in l if p > 0)

# Example 1: 50% red, 50% blue
probs1 = [0.5, 0.5]
print("Entropy (50/50):", entropy(probs1), "bits")

# Example 2: 100% red
probs2 = [1.0, 0.0]
print("Entropy (100% one outcome):", entropy(probs2), "bits")

# Example 3: 70% red, 30% blue
probs3 = [0.9, 0.1]
print("Entropy (70/30):", entropy(probs3), "bits")
# Example 4: 30% red, 70% blue
probs4 = [0.3, 0.7]
print("Entropy (30/70):", entropy(probs4), "bits")


# **7.** Given a list of class labels, calculate the **Gini impurity**.
# **Input:** A list of categorical values
# **Output:** A float (gini value)

# Example 1: 50% red, 50% blue
probs1 = [0.5, 0.5]
probs2=[0.1,0.9]
probs3=[0.9,0.1]

def gini_Impurity(probability):
    return 1-sum(p**2 for p in probability)

print("Gini Impurity",gini_Impurity(probs1))
print("Gini Impurity",gini_Impurity(probs2),gini_Impurity(probs3))