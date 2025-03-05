
#!/bin/bash

# A script to test the ASM generator with various Backstack examples

# Set paths
PYTHON="python3"
MAIN_PY="src/python/main.py"
EXAMPLES_DIR="src/python/examples"

# Function to compile and run a Backstack program
compile_and_run() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .bs)
    
    echo "==== Testing $base_name ===="
    
    # Compile the program
    $PYTHON $MAIN_PY com "$input_file" "${base_name}.asm"
    
    # Check if compilation succeeded
    if [ $? -ne 0 ]; then
        echo "Compilation failed"
        return 1
    fi
    
    # Assemble with NASM
    nasm -f elf64 "${base_name}.asm" -o "${base_name}.o"
    
    # Check if assembly succeeded
    if [ $? -ne 0 ]; then
        echo "Assembly failed"
        return 1
    fi
    
    # Link with GCC
    gcc -no-pie "${base_name}.o" -o "${base_name}"
    
    # Check if linking succeeded
    if [ $? -ne 0 ]; then
        echo "Linking failed"
        return 1
    fi
    
    # Run the program
    echo "Output:"
    ./"${base_name}"
    
    # Clean up
    rm -f "${base_name}.asm" "${base_name}.o" "${base_name}"
    
    echo "Test completed successfully"
    echo
}

# Make sure the script runs from the project root
cd "$(dirname "$0")/.." || exit 1

# Test with examples
for example in "$EXAMPLES_DIR"/*.bs; do
    if [ -f "$example" ]; then
        compile_and_run "$example"
    fi
done

echo "All tests completed!"
