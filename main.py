import sys
import os
import platform
import subprocess

# Add the correct path to the attached_assets module
sys.path.insert(0, os.path.dirname(__file__))

import src.python.backstack as backstack
from stc.python.backstack import simulate_program, read_program_from_args, usage, call_cmd, set_var, get_var

def parse_program(filename):
    """Parse a Backstack program file and return the ops"""
    with open(filename, 'r') as f:
        content = f.read()
    return backstack.parse(content)

def compile_program(program, output_file="output.asm"):
    """Compile a Backstack program to assembly, then assemble and link it"""
    print(f"Compiling to {output_file}...")

    # Initialize the ASM generator
    generator = AsmGenerator()

    # Generate the assembly code
    asm_code = generator.compile_program(program)

    # Write the assembly to file
    with open(output_file, "w") as f:
        f.write(asm_code)

    print(f"Assembly code written to {output_file}")

    # Assemble and link the program
    assemble_and_link(output_file)

def assemble_and_link(asm_file, output_name="output"):
    """Assemble and link the assembly code"""
    # Determine OS-specific commands and extensions
    if platform.system() == "Windows":
        obj_file = f"{output_name}.obj"
        exe_file = f"{output_name}.exe"
        nasm_cmd = f"nasm -f win64 {asm_file} -o {obj_file}"
        link_cmd = f"gcc {obj_file} -o {exe_file}"
    else:  # Linux or macOS
        obj_file = f"{output_name}.o"
        exe_file = output_name
        nasm_cmd = f"nasm -f elf64 {asm_file} -o {obj_file}"
        link_cmd = f"gcc {obj_file} -o {exe_file} -no-pie"

    # Run the assembler
    print(f"Assembling: {nasm_cmd}")
    if subprocess.call(nasm_cmd, shell=True) != 0:
        print("Assembly failed.")
        return False

    # Run the linker
    print(f"Linking: {link_cmd}")
    if subprocess.call(link_cmd, shell=True) != 0:
        print("Linking failed.")
        return False

    print(f"Executable created: {exe_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "sim":
        # Simulate the program
        program = read_program_from_args(sys.argv[2:])
        simulate_program(program)
    elif cmd == "com":
        # Compile the program to assembly
        from attached_assets.asm_generator import AsmGenerator

        if len(sys.argv) < 3:
            print("Error: No input file specified")
            usage()
            sys.exit(1)

        program = parse_program(sys.argv[2])
        compile_program(program)
    else:
        print(f"Unknown command: {cmd}")
        usage()
        sys.exit(1)
