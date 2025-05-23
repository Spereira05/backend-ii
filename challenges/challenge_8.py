# Challenge 8: Factorial function with pytest parametrization

def factorial(n):
    """
    Calculate the factorial of a number using recursion.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n (n!)
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    # Type checking
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    
    # Check for negative input
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Base cases
    if n == 0 or n == 1:
        return 1
    
    # Recursive case
    return n * factorial(n - 1)

# If this file is run directly, demonstrate the function
if __name__ == "__main__":
    # Print some example factorial calculations
    for i in range(6):
        print(f"{i}! = {factorial(i)}")
    
    print("\nTo run the tests for this function:")
    print("1. Create a file named 'test_challenge_8.py' with the test code")
    print("2. Run 'pytest test_challenge_8.py -v' in the terminal")

"""
To test this function, create a file named 'test_challenge_8.py' with the following content:

import pytest
from challenge_8 import factorial

# Basic test cases
def test_factorial_base_cases():
    assert factorial(0) == 1
    assert factorial(1) == 1

def test_factorial_small_numbers():
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120

# Parameterized test with multiple inputs and expected results
@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (8, 40320),
    (9, 362880),
    (10, 3628800),
])
def test_factorial_parametrized(n, expected):
    assert factorial(n) == expected

# Test error cases
def test_factorial_raises_for_negative():
    with pytest.raises(ValueError):
        factorial(-1)
    
    with pytest.raises(ValueError):
        factorial(-5)

def test_factorial_raises_for_non_integer():
    with pytest.raises(TypeError):
        factorial(2.5)
    
    with pytest.raises(TypeError):
        factorial("3")
"""