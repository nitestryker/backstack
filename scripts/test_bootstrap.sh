
#!/bin/bash

# Script to test the bootstrap compiler

# Set the path to your bootstrap compiler
BOOTSTRAP_FILE="../src/bootstrap/bootstrap_compiler.bs"

# Check if the file exists
if [ ! -f "$BOOTSTRAP_FILE" ]; then
    echo "Error: Bootstrap compiler file not found at $BOOTSTRAP_FILE"
    exit 1
fi

echo "Running bootstrap compiler..."
python src/python/main.py sim "$BOOTSTRAP_FILE"

# You can also compile it to assembly if you want to test that aspect
echo -e "\nCompiling bootstrap compiler to assembly..."
python src/python/main.py com "$BOOTSTRAP_FILE" bootstrap_output.asm

# Check if NASM is available
if command -v nasm &> /dev/null; then
    echo -e "\nAssembling with NASM..."
    
    # Detect OS for proper format
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        ASM_FORMAT="win64"
    else
        ASM_FORMAT="elf64"
    fi
    
    nasm -f $ASM_FORMAT bootstrap_output.asm -o bootstrap_output.o
    
    if [ $? -eq 0 ]; then
        echo "Assembly successful!"
        
        echo -e "\nLinking with GCC..."
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            gcc bootstrap_output.o -o bootstrap_output.exe
            echo "If successful, you can run: ./bootstrap_output.exe"
        else
            gcc -no-pie bootstrap_output.o -o bootstrap_output
            echo "If successful, you can run: ./bootstrap_output"
        fi
    fi
else
    echo "NASM not found. Could not assemble the generated code."
fi

echo -e "\nBootstrap compiler test complete!"
