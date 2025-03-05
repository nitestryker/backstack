
#!/usr/bin/env python3

import os
import sys
import argparse

# Add correct path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import backstack modules
from backstack import simulate_program, read_program_from_args, read_program_from_file, usage, call_cmd
from asm_generator import AsmGenerator

def main():
    """Main entry point for the Backstack interpreter and compiler"""
    if len(sys.argv) < 2:
        usage()
        return
        
    cmd = sys.argv[1]
    
    if cmd == "help":
        usage()
    elif cmd == "sim":
        # Simulate the program
        program = read_program_from_args(sys.argv[2:])
        simulate_program(program)
    elif cmd == "com":
        # Compile the program to assembly
        if len(sys.argv) < 3:
            print("ERROR: Source file required")
            usage()
            return
            
        source_file = sys.argv[2]
        
        # Default output is input filename with .asm extension
        output_file = source_file.rsplit(".", 1)[0] + ".asm" if len(sys.argv) < 4 else sys.argv[3]
        
        # Read program from file
        program = read_program_from_file(source_file)
        if not program:
            return
            
        # Generate assembly code
        generator = AsmGenerator()
        asm_code = generator.compile_program(program)
        
        # Write to output file
        try:
            with open(output_file, "w") as f:
                f.write(asm_code)
            print(f"Compiled to: {output_file}")
        except Exception as e:
            print(f"ERROR: Failed to write assembly output: {e}")
            return
            
    elif cmd == "run":
        # Compile and run the program
        if len(sys.argv) < 3:
            print("ERROR: Source file required")
            usage()
            return
            
        source_file = sys.argv[2]
        base_name = os.path.basename(source_file).rsplit(".", 1)[0]
        
        # Read program from file
        program = read_program_from_file(source_file)
        if not program:
            return
            
        # Generate assembly code
        generator = AsmGenerator()
        asm_code = generator.compile_program(program)
        
        # Write to temporary assembly file
        asm_file = f"{base_name}.asm"
        obj_file = f"{base_name}.o"
        exe_file = base_name if os.name != "nt" else f"{base_name}.exe"
        
        try:
            with open(asm_file, "w") as f:
                f.write(asm_code)
                
            # Assemble and link
            if os.name == "nt":  # Windows
                nasm_ret = call_cmd("nasm", ["-f", "win64", asm_file, "-o", obj_file])
                if nasm_ret != 0:
                    print("ERROR: Failed to assemble program")
                    return
                    
                link_ret = call_cmd("link", [obj_file, "/SUBSYSTEM:CONSOLE", f"/OUT:{exe_file}"])
                if link_ret != 0:
                    print("ERROR: Failed to link program")
                    return
            else:  # Linux/Unix
                nasm_ret = call_cmd("nasm", ["-f", "elf64", asm_file, "-o", obj_file])
                if nasm_ret != 0:
                    print("ERROR: Failed to assemble program")
                    return
                    
                link_ret = call_cmd("gcc", ["-no-pie", obj_file, "-o", exe_file])
                if link_ret != 0:
                    print("ERROR: Failed to link program")
                    return
                    
            # Run the compiled program
            print(f"Running: {exe_file}")
            run_ret = call_cmd(f"./{exe_file}" if os.name != "nt" else exe_file)
            if run_ret != 0:
                print(f"Program exited with code: {run_ret}")
                
        except Exception as e:
            print(f"ERROR: Failed to compile and run program: {e}")
            return
    else:
        print(f"ERROR: Unknown command: {cmd}")
        usage()

if __name__ == "__main__":
    main()
