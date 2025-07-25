"""
probability.py - Probability functions for mlmath library
"""

def conditional_probability(events):
    """
    Calculate conditional probability P(A|B) = P(A and B) / P(B)

    Args:
        events (dict): A dictionary with keys:
                       - 'A_and_B': Count of A and B happening together
                       - 'B': Count of B happening
                       - 'total': Total number of trials

    Returns:
        float: Conditional probability P(A|B)

    Example:
        >>> events = {'A_and_B': 30, 'B': 50, 'total': 100}
        >>> conditional_probability(events)
        0.6
    """
    P_A_and_B = events['A_and_B'] / events['total']
    P_B = events['B'] / events['total']
    if P_B == 0:
        raise ZeroDivisionError("P(B) is zero, cannot divide by zero.")
    return P_A_and_B / P_B
