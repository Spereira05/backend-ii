import unittest

class TestMathFunctions(unittest.TestCase):
    def test_addition(self):
        """Test that addition works correctly"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(0 + 0, 0)
        self.assertEqual(-1 + 1, 0)
        self.assertEqual(100 + 200, 300)
    
    def test_subtraction(self):
        """Test that subtraction works correctly"""
        self.assertEqual(5 - 3, 2)
        self.assertEqual(10 - 10, 0)
        self.assertEqual(0 - 5, -5)
    
    def test_multiplication(self):
        """Test that multiplication works correctly"""
        self.assertEqual(3 * 4, 12)
        self.assertEqual(0 * 100, 0)
        self.assertEqual(-2 * 3, -6)
    
    def test_division(self):
        """Test that division works correctly"""
        self.assertEqual(10 / 2, 5)
        self.assertEqual(8 / 4, 2)
        self.assertEqual(1 / 4, 0.25)
        
    def test_division_by_zero(self):
        """Test that division by zero raises an exception"""
        with self.assertRaises(ZeroDivisionError):
            result = 5 / 0

if __name__ == '__main__':
    unittest.main()