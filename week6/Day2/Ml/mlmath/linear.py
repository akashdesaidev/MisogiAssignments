"""
linear.py - Linear algebra functions for mlmath library
"""

def dot_product(a, b):
    """
    Calculate the dot product of two vectors.

    Args:
        a (list of numbers): First vector.
        b (list of numbers): Second vector.

    Returns:
        float: The dot product.

    Example:
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32
    """
    return sum(x * y for x, y in zip(a, b))


def matrix_multiply(A, B):
    """
    Multiply two matrices.

    Args:
        A (list of list of numbers): Matrix A of size m x n.
        B (list of list of numbers): Matrix B of size n x p.

    Returns:
        list of list of numbers: Resulting matrix of size m x p.

    Example:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> matrix_multiply(A, B)
        [[19, 22], [43, 50]]
    """
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in A must match rows in B.")

    result = []
    for row in A:
        new_row = []
        for col in zip(*B):
            new_row.append(dot_product(row, col))
        result.append(new_row)
    return result
