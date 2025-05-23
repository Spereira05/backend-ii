# Exercise 8: Testing with pytest
# Function to be tested
def multiply(a, b):
    """
    Multiply two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The product of a and b
    """
    return a * b

# If this file is run directly, demonstrate the function
if __name__ == "__main__":
    # Example usage
    num1 = 5
    num2 = 7
    result = multiply(num1, num2)
    print(f"{num1} × {num2} = {result}")
    
    # Another example with floating point numbers
    num3 = 3.5
    num4 = 2.0
    result2 = multiply(num3, num4)
    print(f"{num3} × {num4} = {result2}")

    print("\nTo run the tests for this function:")
    print("1. Create a file named 'test_exercise_8.py' with the test code")
    print("2. Run 'pytest test_exercise_8.py -v' in the terminal")

"""
To test this function, create a file named 'test_exercise_8.py' with the following content:

import pytest
from exercise_8 import multiply

def test_multiply_integers():
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0
    assert multiply(-2, 4) == -8
    assert multiply(-3, -5) == 15

def test_multiply_floats():
    assert multiply(2.5, 3.0) == 7.5
    assert multiply(0.1, 0.2) == pytest.approx(0.02)  # Using approx for floating point comparison

def test_multiply_zero():
    assert multiply(0, 0) == 0
    assert multiply(5, 0) == 0
    assert multiply(0, -5) == 0
"""