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

def test_multiply_types():
    # Test that the function works with different numeric types
    assert multiply(2, 3.5) == 7.0
    assert multiply(1.5, 2) == 3.0
    
    # Test with larger numbers
    assert multiply(1000, 1000) == 1000000

# Parameterized test example
@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 1),
    (2, 3, 6),
    (0, 5, 0),
    (-2, -3, 6),
    (2.5, 2, 5.0),
])
def test_multiply_parametrized(a, b, expected):
    assert multiply(a, b) == expected