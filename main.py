import sys
import os
import src.backstack as backstack
from src.backstack import simulate_program, compile_program, read_program_from_args, usage, call_cmd, set_var, get_var

def main():
    # Make sure the directory structure exists
    if not os.path.exists('src'):
        print("ERROR: 'src' directory not found")
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
        compile_program(program, "output.asm")
        call_cmd(["nasm", "-g", "-fwin64", "output.asm", "-o", "output.o"])
        call_cmd(["gcc", "output.o", "-o", "output.exe", "-nostdlib", "-lkernel32", "-lmsvcrt", "-Wl,--subsystem,console", "-Wl,-e,_start"])
    else:
        usage()
        print(f"ERROR: Unknown subcommand '{subcommand}'")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
