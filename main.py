
import sys
import os
import platform

# Add the correct path to the attached_assets module
sys.path.insert(0, os.path.dirname(__file__))

import src.python.backstack as backstack
from src.python.backstack import simulate_program, read_program_from_args, usage, call_cmd, set_var, get_var, parse_program
from src.python.asm_generator import AsmGenerator

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

def assemble_and_link(asm_file):
    """Assemble and link the generated assembly code"""
    base_name = os.path.splitext(asm_file)[0]
    obj_file = f"{base_name}.o"
    
    # Determine executable extension based on platform
    if platform.system() == "Windows":
        exe_file = f"{base_name}.exe"
    else:
        exe_file = base_name
    
    # Determine commands based on platform
    if platform.system() == "Windows":
        # Windows commands
        print("Assembling with NASM...")
        assemble_cmd = f"nasm -f win64 {asm_file} -o {obj_file}"
        
        print("Linking with GCC...")
        link_cmd = f"gcc {obj_file} -o {exe_file}"
    else:
        # Linux/macOS commands
        print("Assembling with NASM...")
        assemble_cmd = f"nasm -f elf64 {asm_file} -o {obj_file}"
        
        print("Linking with GCC...")
        link_cmd = f"gcc {obj_file} -o {exe_file} -no-pie"
    
    # Execute commands
    print(f"Running: {assemble_cmd}")
    if os.system(assemble_cmd) != 0:
        print("Error: Assembly failed")
        return False
    
    print(f"Running: {link_cmd}")
    if os.system(link_cmd) != 0:
        print("Error: Linking failed")
        return False
    
    print(f"Successfully compiled to {exe_file}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "sim":
        # Simulate mode
        # Check if input is a file or direct input
        if len(sys.argv) > 2 and os.path.isfile(sys.argv[2]):
            with open(sys.argv[2], 'r') as f:
                program_text = f.read()
            program = parse_program(program_text)
        else:
            program = read_program_from_args(sys.argv[2:])
        
        simulate_program(program)
    
    elif command == "com":
        # Compile mode
        if len(sys.argv) < 3:
            print("Error: File path required for compile mode")
            usage()
            sys.exit(1)
        
        # Read program from file
        with open(sys.argv[2], 'r') as f:
            program_text = f.read()
        
        # Parse the program
        program = parse_program(program_text)
        
        # Compile the program
        compile_program(program)
    
    else:
        print(f"Unknown command: {command}")
        usage()
        sys.exit(1)

def main():
    # Make sure the directory structure exists
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'attached_assets')):
        print("ERROR: 'attached_assets' directory not found")
        return 1
        
    if len(sys.argv) < 2:
        usage()
        print("ERROR: No subcommand provided")
        return 1
        
    subcommand = sys.argv[1]
    
    if len(sys.argv) < 3:
        usage()
        print("ERROR: No program instructions provided")
        return 1
        
    program = read_program_from_args(sys.argv[2:])
    
    if subcommand == "sim":
        # Run without debug messages by default
        debug_mode = "--debug" in sys.argv
        simulate_program(program, debug=debug_mode)
    elif subcommand == "com":
        # Detect platform for appropriate compilation flags
        system = platform.system()
        output_asm = "output.asm"
        output_obj = "output.o"
        output_exe = "output.exe" if system == "Windows" else "output"
        
        # Generate assembly code
        compile_program(program, output_asm)
        
        # Compile assembly based on platform
        if system == "Windows":
            call_cmd(["nasm", "-g", "-fwin64", output_asm, "-o", output_obj])
            call_cmd(["gcc", output_obj, "-o", output_exe, "-nostdlib", "-lkernel32", "-lmsvcrt", 
                     "-Wl,--subsystem,console", "-Wl,-e,_start"])
        else:  # Linux and macOS
            if system == "Darwin":  # macOS
                call_cmd(["nasm", "-g", "-fmacho64", output_asm, "-o", output_obj])
                call_cmd(["gcc", output_obj, "-o", output_exe])
            else:  # Linux
                call_cmd(["nasm", "-g", "-felf64", output_asm, "-o", output_obj])
                call_cmd(["gcc", output_obj, "-o", output_exe, "-no-pie"])
        
        print(f"Compilation complete! Executable created at: {output_exe}")
    else:
        usage()
        print(f"ERROR: Unknown subcommand '{subcommand}'")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
