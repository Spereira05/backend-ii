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

# Edge case test for larger numbers
def test_factorial_larger_numbers():
    # Test a few larger numbers
    assert factorial(12) == 479001600
    assert factorial(15) == 1307674368000

# Test that recursion doesn't cause stack overflow for reasonable inputs
def test_factorial_moderate_recursion_depth():
    # This should not cause a stack overflow
    result = factorial(20)
    assert result == 2432902008176640000