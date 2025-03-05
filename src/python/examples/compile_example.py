
#!/usr/bin/env python3

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.python.backstack import read_program_from_file, tokenize, parse_program
from src.python.asm_generator import AsmGenerator

def compile_example(example_file, output_file):
    """
    Compile a Backstack example file to assembly
    
    Args:
        example_file (str): Path to the Backstack source file
        output_file (str): Path for the output assembly file
    """
    print(f"Compiling {example_file} to {output_file}...")
    
    # Read the program from file
    with open(example_file, 'r') as f:
        program_text = f.read()
    
    # Parse the program
    tokens = tokenize(program_text.splitlines())
    program = parse_program(tokens)
    
    # Generate assembly
    generator = AsmGenerator()
    asm_code = generator.compile_program(program)
    
    # Write to output file
    with open(output_file, 'w') as f:
        f.write(asm_code)
    
    print(f"Assembly code generated successfully in {output_file}")
    print("\nTo assemble and run this code (on Linux):")
    print(f"  nasm -f elf64 {output_file} -o output.o")
    print("  gcc -no-pie output.o -o output")
    print("  ./output")
    print("\nOr on Windows:")
    print(f"  nasm -f win64 {output_file} -o output.o")
    print("  gcc output.o -o output.exe")
    print("  output.exe")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compile_example.py <example_file> [output_file]")
        sys.exit(1)
    
    example_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.asm"
    
    compile_example(example_file, output_file)
