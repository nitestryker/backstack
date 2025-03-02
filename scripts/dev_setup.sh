
#!/bin/bash

# Development environment setup script for Backstack

echo "Setting up Backstack development environment..."

# Make sure all scripts are executable
chmod +x src/bootstrap/build_compiler.sh

# Build the C implementation
echo "Building Backstack C implementation..."
cd src/c_code
make

# Run a simple test
echo "Running a simple test..."
cd ../../
python src/python/main.py sim '5 3 + dump'

echo "Development environment setup complete!"
