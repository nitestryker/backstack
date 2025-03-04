
# Backstack Assembly Code Generation

This document describes the assembly code generation capabilities of Backstack.

## Overview

Backstack can translate Backstack programs into x86-64 assembly code, which can then be assembled and linked to create native executables. This allows Backstack programs to run efficiently without requiring an interpreter.

## Supported Platforms

The assembly generator supports the following platforms:

- Windows (64-bit, using NASM and GCC)
- Linux (64-bit, using NASM and GCC)
- macOS (64-bit, using NASM and GCC)

## Usage

To compile a Backstack program to an executable:

```bash
python src/python/main.py com path/to/your/program.bs
```

This command will:
1. Parse the Backstack program
2. Generate assembly code (output.asm)
3. Assemble the code to an object file (output.o)
4. Link the object file to create an executable (output or output.exe)

## Supported Operations

The assembly generator supports the following Backstack operations:

### Basic Operations
- Integer literals
- String literals
- Boolean literals
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Modulo (%)
- Dump (print)

### Bitwise Operations
- Bitwise AND (&)
- Bitwise OR (|)
- Bitwise XOR (^)
- Bitwise NOT (~)

### Comparison Operations
- Equality (==)
- Inequality (!=)
- Greater than (>)
- Less than (<)

### Control Flow
- If statements
- While loops

### Variables
- Set variable (!var)
- Get variable (var)

## Implementation Details

The assembly generator produces code that follows the x86-64 calling conventions for the target platform:

- Windows: Uses the Microsoft x64 calling convention
- Linux/macOS: Uses the System V AMD64 ABI

### Stack Management

The Backstack runtime stack is implemented using the hardware stack (via PUSH and POP instructions). Each value occupies 8 bytes on the stack (64 bits).

### Memory Management

String literals are stored in the data section of the assembly file, and references to these strings are pushed onto the stack as needed.

### Printing

The generator implements helper functions for printing different types of values:
- print_int: Prints integer values
- print_bool: Prints boolean values as "true" or "false"
- print_string: Prints string values

## Testing

You can test the assembly generation with the included test script:

```bash
./scripts/test_asm_gen.sh
```

This script compiles and runs a test program that exercises various features of the assembly generator.

## Extending the Generator

To add support for additional Backstack operations, you need to:

1. Add a new method to the AsmGenerator class in src/python/attached_assets/asm_generator.py
2. Update the compile_op method to call your new method for the corresponding operation

For example, to add support for a new "SQRT" operation, you would:

1. Add a compile_sqrt method to AsmGenerator
2. Update compile_op to call compile_sqrt when it encounters OP_SQRT
