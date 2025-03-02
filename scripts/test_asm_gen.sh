
#!/bin/bash

# Script to test ASM generation

# Change to project root directory
cd "$(dirname "$0")/.."

# Compile the test file
echo "Compiling examples/asm_test.bs..."
python "$(cygpath -w main.py)" compile examples/asm_test.bs
# Check if compilation succeeded
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Run the compiled program if available
if [ -f "output" ]; then
    echo "Running output..."
    ./output
elif [ -f "output.exe" ]; then
    echo "Running output.exe..."
    ./output.exe
else
    echo "No executable found!"
    exit 1
fi

echo "ASM generation test completed!"
