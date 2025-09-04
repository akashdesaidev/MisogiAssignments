# - Given a function `f(x)`, compute the **numerical derivative** at a point using finite difference.
#     **Input**: Function as lambda, and a float
#     **Output**: A float (derivative)
# The derivative of a function at a point gives the rate of change (slope) of the function at that point.
import numpy  as np
func=lambda x:x**2
point=3.0

def derivative(func,x,h=0.0001):
    return (func(x+h)-func(x-h))/(2*h)
print("derivateive",derivative(func,point))


#2 - Implement **gradient descent** for a simple univariate function.    
#     **Input**: Function, derivative, learning rate, iterations   
#     **Output**: Minimized value of `x`

# Gradient descent is an optimization algorithm used to minimize a function by iteratively moving in the direction of the steepest descent, as defined by the negative of the gradient.
# For a univariate function f(x), the update rule is:
#   x_new = x_old - learning_rate * f'(x_old)
# Here, f'(x) is the derivative of f at x, and learning_rate controls the step size.
# The process is repeated for a number of iterations or until convergence.
# Gradient Descent is an iterative optimization algorithm used to minimize a function by updating its parameters in the direction opposite to the gradient of the function.
def gradient_descent(func, derivative, start_x, learning_rate, iterations=10, tolerance=1e-6):
    x = start_x
    for i in range(iterations):
        grad = derivative(func, x)
        if abs(grad) < tolerance:   # convergence check
            print(f"Converged at iteration {i+1}")
            break
        x_new = x - learning_rate * grad
        if abs(x_new - x) < tolerance:   # optional check
            print(f"Small parameter change at iteration {i+1}")
            break
        x = x_new
        print(f"Iter {i+1}: x = {x:.6f}, f(x) = {func(x):.6f}")
    return x

print("Gradient Decent",gradient_descent(func,derivative,3,0.1,1000,1e-6))

# - Given a dataset with one feature and one target, implement **cost function for linear regression**.   
#     **Input**: Two lists   
#     **Output**: Cost value

# For linear regression, the most common cost function is the Mean Squared Error (MSE).
# What it Measures
# The cost function measures how far our predictions are from the actual values.
# Lower cost → better model fit
# Higher cost → worse model fit
actual=[1,2,3]
pred=[1.1,2.1,3.2]

def cost_Func(y_true,y_pred):
    m=len(y_true)
    sum=0
    for i in range(len(y_true)):
        sum+=(y_pred[i] - y_true[i])**2
    return sum/(2*m)

print("cost" ,cost_Func(actual,pred))



# - Given two lists (features, targets), compute the **gradient** of MSE loss in linear regression.    
#     **Input**: Two lists and initial weights   
#     **Output**: Gradient values

def compute_gradient(x, y, w, b):
    m = len(x)
    dw, db = 0, 0
    for i in range(m):
        y_pred = w * x[i] + b
        dw += (y_pred - y[i]) * x[i]
        db += (y_pred - y[i])
    dw /= m
    db /= m
    return dw, db

# Example
dw, db = compute_gradient(x=actual, y=pred, w=0, b=0)
print("Gradient:", dw, db)
