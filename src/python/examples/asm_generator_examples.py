#!/usr/bin/env python3

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.python.backstack import read_program_from_file, tokenize, parse_program
from src.python.asm_generator import AsmGenerator

def generate_asm_from_file(input_file, output_file):
    """
    Generate assembly code from a Backstack file

    Args:
        input_file (str): Path to the Backstack source file
        output_file (str): Path to write the generated assembly
    """
    program = read_program_from_file(input_file)
    if not program:
        print(f"Error: Could not read program from {input_file}")
        return False

    generator = AsmGenerator()
    asm_code = generator.compile_program(program)

    try:
        with open(output_file, "w") as f:
            f.write(asm_code)
        print(f"Successfully compiled {input_file} to {output_file}")
        return True
    except Exception as e:
        print(f"Error writing assembly output: {e}")
        return False

def generate_asm_from_code(code_string, output_file):
    """
    Generate assembly code from a Backstack code string

    Args:
        code_string (str): Backstack code as a string
        output_file (str): Path to write the generated assembly
    """
    tokens = tokenize(code_string)
    program = parse_program(tokens)

    generator = AsmGenerator()
    asm_code = generator.compile_program(program)

    try:
        with open(output_file, "w") as f:
            f.write(asm_code)
        print(f"Successfully compiled code to {output_file}")
        return True
    except Exception as e:
        print(f"Error writing assembly output: {e}")
        return False

# Example 1: Generate assembly from a simple program string
simple_program = """
5 10 + dump
20 5 - dump
3 4 * dump
"""

# Example 2: Generate assembly for a factorial program
factorial_program = """
# Recursive factorial function
fun:factorial
  dup 1 <= if
    drop 1 return  # Base case: return 1
  else
    dup 1 - call:factorial * return  # Recursive case
  endif
fun_end

5 call:factorial dump  # Calculate and print 5! (120)
"""

if __name__ == "__main__":
    # Example usages
    print("Example 1: Generating assembly from simple arithmetic")
    generate_asm_from_code(simple_program, "simple_arithmetic.asm")

    print("\nExample 2: Generating assembly from factorial program")
    generate_asm_from_code(factorial_program, "factorial.asm")

    print("\nExample 3: Generating assembly from an existing file")
    # Assuming there's a file named 'asm_test.bs' in the examples directory
    input_file = os.path.join(os.path.dirname(__file__), "asm_test.bs")
    if os.path.exists(input_file):
        generate_asm_from_file(input_file, "asm_test.asm")
    else:
        print(f"Example file {input_file} not found")