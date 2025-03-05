
import sys
import os
import unittest

# Modify the path to match the correct folder structure
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules to test
from src.python import backstack

class TestBackstack(unittest.TestCase):
    def test_basic_operations(self):
        # Test basic stack operations
        program = [
            backstack.push(5),
            backstack.push(3),
            backstack.plus()
        ]
        
        # Run the program in a controlled environment
        stack = []
        for op in program:
            if op[0] == backstack.OP_PUSH:
                stack.append(op[1])
            elif op[0] == backstack.OP_PLUS:
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
        
        # Check the result
        self.assertEqual(stack[0], 8, "Basic addition should work correctly")

if __name__ == '__main__':
    unittest.main()
