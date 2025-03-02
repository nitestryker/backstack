#!/bin/bash

# Build script for Backstack compiler

echo "Building Backstack compiler..."

# Step 1: Build the C implementation
gcc -Wall -g -o backstack.exe src/c_code/backstack.c

if [ $? -ne 0 ]; then
    echo "Error: Failed to compile backstack.c"
    exit 1
fi

echo "C implementation compiled successfully."

# Step 2: Test basic functionality
echo "Testing basic functionality..."
./backstack.exe sim examples/simple_bitwise.bs

echo "Build complete. You can now use ./backstack.exe sim <file> or ./backstack.exe com <file>"
