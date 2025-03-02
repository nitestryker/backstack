
# Backstack Language Documentation

## Introduction

Backstack is a stack-based programming language with a simple, readable syntax inspired by Forth. This document provides a comprehensive guide to programming in Backstack, with explanations and examples for all major language features.

## Getting Started

### Running a Backstack Program

To run a Backstack program, use the `sim` (simulate) command:

```
python main.py sim your_program.bs
```

You can also compile a program to assembly using the `com` (compile) command:

```
python main.py com your_program.bs
```

### Hello World

Here's a simple "Hello World" program in Backstack:

```
"Hello, World!"  # Push string to stack
dump             # Print top value from stack
```

## Core Concepts

### Stack-Based Execution

Backstack is a stack-based language, meaning operations work on values stored on a stack.

- Values are pushed onto the stack by writing them directly
- Operations generally pop values from the stack, perform calculations, and push results back

Example:

```
5    # Push 5 onto stack
3    # Push 3 onto stack
+    # Pop 5 and 3, add them, push 8
dump # Print the result (8)
```

Key stack manipulation operations:

- `dup` - Duplicate the top value on the stack
- `swap` - Swap the top two values on the stack
- `drop` - Remove the top value from the stack
- `over` - Copy the second value on the stack to the top
- `rot` - Rotate the top three values on the stack

Example:

```
5 7    # Stack: 5 7
dup    # Stack: 5 7 7 (duplicated top value)
swap   # Stack: 5 7 7 → 5 7 7 → 7 5 7
drop   # Stack: 7 5 (dropped top value)
dump   # Prints: 5
```

### Basic Arithmetic

Backstack supports standard arithmetic operations:

- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulus
- `**` - Exponentiation

Example:

```
10 3 +   # 13
20 5 -   # 15
4 5 *    # 20
20 4 /   # 5
10 3 %   # 1
2 8 **   # 256
```

## String Manipulation

Backstack provides robust string operations for working with text data.

### String Literals

Define strings using double quotes:

```
"Hello, Backstack!"
```

### String Operations

- `str_concat` - Concatenate two strings
- `str_length` - Get the length of a string
- `str_slice` - Extract a substring
- `str_contains` - Check if a string contains another string
- `str_split` - Split a string by a delimiter
- `str` - Convert a value to a string

Examples:

```
# String concatenation
"Hello, " "world!" str_concat  # "Hello, world!"

# String length
"Backstack" str_length  # 9

# String slice (substring)
"Hello, world!" 7 12 str_slice  # "world"

# String contains
"Hello, world!" "world" str_contains  # 1 (true)

# Convert number to string
42 str  # "42"
```

## Variable Support

Backstack allows storing and retrieving values using named variables.

### Setting Variables

To store a value in a variable, use `set:variable_name`:

```
42 set:answer  # Store 42 in variable "answer"
```

### Getting Variables

To retrieve a value from a variable, use `get:variable_name`:

```
get:answer  # Push the value of "answer" (42) onto the stack
```

Example:

```
10 set:x      # Store 10 in x
20 set:y      # Store 20 in y
get:x get:y + # Add x and y (10 + 20)
dump          # Print the result (30)
```

## Control Flow

### Conditionals (if/else)

Backstack supports conditional branching with `if`/`else`/`endif` structure:

```
# Basic if statement
condition if
  # Code executed if condition is true (non-zero)
endif

# If-else statement
condition if
  # Code executed if condition is true
else
  # Code executed if condition is false
endif
```

Example:

```
# Check if a number is positive
dup 0 > if
  "Positive number" dump
else
  "Zero or negative number" dump
endif
```

### Comparison Operators

- `==` - Equal
- `!=` - Not equal
- `>` - Greater than
- `<` - Less than
- `<=` - Less than or equal
- `>=` - Greater than or equal

### Loops

Backstack provides two main loop structures:

#### While-Repeat Loop

```
while
  # Loop code
  # Leave condition on stack (0 = exit, non-zero = continue)
repeat
```

Example (counting from 1 to 5):

```
1 set:counter         # Initialize counter

while
  get:counter dup     # Get counter value and duplicate it
  dump                # Print current counter
  
  1 + set:counter     # Increment counter
  
  get:counter 5 <=    # Check if counter <= 5
repeat                # Loop back if true
```

#### For-Next Loop

```
end_value start_value for
  # Loop code (current value is on stack)
next
```

Example (sum numbers 1 to 10):

```
0 set:sum          # Initialize sum

10 1 for           # Loop from 1 to 10
  dup get:sum +    # Add current number to sum
  set:sum          # Update sum
next

get:sum dump       # Print final sum (55)
```

## Functions

### Defining Functions

Define a function using `fun:name` and `fun_end`:

```
fun:function_name
  # Function body
  return
fun_end
```

### Calling Functions

Call a function using `call:name`:

```
call:function_name
```

Example (factorial function):

```
# Recursive factorial function
fun:factorial
  dup 1 <= if
    drop 1 return  # Base case: return 1
  else
    dup 1 - call:factorial * return  # Recursive case
  endif
fun_end

5 call:factorial dump  # Calculate and print 5! (120)
```

## Array Operations

Backstack provides operations for creating and manipulating arrays.

### Creating Arrays

Create a new array using `array_new` with the size:

```
5 array_new  # Create array of size 5
```

### Array Operations

- `array_set` - Set a value at an index
- `array_get` - Get a value from an index
- `array_len` - Get the length of an array

Example:

```
5 array_new set:arr  # Create array of size 5 and store reference

# Set values
get:arr 0 10 array_set  # arr[0] = 10
get:arr 1 20 array_set  # arr[1] = 20
get:arr 2 30 array_set  # arr[2] = 30

# Get values
get:arr 1 array_get dump  # Print arr[1] (20)

# Get array length
get:arr array_len dump  # Print array length (5)
```

## File I/O

Backstack supports file operations for reading and writing data.

### File Operations

- `file_open` - Open a file (returns a file handle)
- `file_close` - Close a file
- `file_read` - Read entire file contents
- `file_write` - Write to a file
- `file_append` - Append to a file

Example:

```
# Write to a file
"test.txt" "w" file_open set:file
get:file "Hello, file I/O!" file_write
get:file file_close

# Read from a file
"test.txt" "r" file_open set:file
get:file file_read dump  # Print file contents
get:file file_close
```

## Bitwise Operations

Backstack supports various bitwise operations for low-level programming.

### Bitwise Operators

- `&` - Bitwise AND
- `|` - Bitwise OR
- `^` - Bitwise XOR
- `~` - Bitwise NOT
- `<<` - Shift left
- `>>` - Shift right

Example:

```
# Bitwise AND: 12 & 7 = 4
12 7 & dump  # Binary: 1100 & 0111 = 0100 (4)

# Bitwise OR: 12 | 7 = 15
12 7 | dump  # Binary: 1100 | 0111 = 1111 (15)

# Bitwise XOR: 12 ^ 7 = 11
12 7 ^ dump  # Binary: 1100 ^ 0111 = 1011 (11)

# Bitwise NOT: ~5 = -6
5 ~ dump     # Binary (8-bit): ~00000101 = 11111010 (-6)

# Shift left: 5 << 2 = 20
5 2 << dump  # Binary: 00101 << 2 = 10100 (20)

# Shift right: 20 >> 2 = 5
20 2 >> dump # Binary: 10100 >> 2 = 00101 (5)
```

## Input/Output

### Output

Print a value using `dump`:

```
"Hello" dump  # Print "Hello"
```

### Input

Get user input using `input`:

```
"Enter your name: " input  # Shows prompt and gets input
```

## Example Programs

### Calculate Fibonacci Numbers

```
# Recursive Fibonacci function
fun:fibonacci
  dup 1 <= if
    # Base case for n <= 1
    return
  else
    # Recursive case: fib(n-1) + fib(n-2)
    dup 1 - call:fibonacci
    swap 2 - call:fibonacci
    + return
  endif
fun_end

# Calculate fibonacci(10)
10 call:fibonacci dump  # 55
```

### Strong Password Generator

```
# Initialize random seed
1234567 set:seed

# Function to generate a random number
fun:random
  get:seed  # Get current seed
  1103515245 * 12345 + 2147483647 %  # LCG algorithm
  dup set:seed  # Update seed
  return
fun_end

# Function to get a random character from a string
fun:random_char
  # Stack: string
  dup str_length  # Get string length
  call:random swap %  # Random index between 0 and length-1
  # Stack: string index
  swap 2dup  # Stack: index string index
  1 + str_slice  # Get char at index
  # Return the character
  return
fun_end

# Generate password of given length
fun:generate_password
  # Stack: length
  set:length  # Store desired password length
  "" set:password  # Initialize empty password
  
  # Character sets
  "abcdefghijklmnopqrstuvwxyz" set:lowercase
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ" set:uppercase
  "0123456789" set:numbers
  "!@#$%^&*()-_=+[]{}|;:,.<>?" set:symbols
  
  # Ensure at least one character from each set
  get:lowercase call:random_char set:password
  get:uppercase call:random_char get:password str_concat set:password
  get:numbers call:random_char get:password str_concat set:password
  get:symbols call:random_char get:password str_concat set:password
  
  # Fill the rest of the password
  get:length 4 - set:remaining  # 4 characters already added
  
  # Combine all character sets
  get:lowercase get:uppercase str_concat 
  get:numbers str_concat get:symbols str_concat
  set:all_chars
  
  # Add remaining characters
  0 set:i
  while
    get:all_chars call:random_char
    get:password str_concat
    set:password
    
    get:i 1 + set:i
    get:i get:remaining <
  repeat
  
  get:password return
fun_end

# Generate a 12-character password
12 call:generate_password dump
```

## Best Practices

1. **Stack Hygiene**: Be mindful of what's on the stack. Clean up unused values with `drop`.

2. **Comments**: Use comments (`#`) to document your code, especially for complex operations.

3. **Variable Naming**: Use descriptive variable names for readability.

4. **Function Structure**: Design functions with clear inputs and outputs.

5. **Error Handling**: Check for error conditions, especially in file operations.

## Common Pitfalls

1. **Stack Underflow**: Trying to pop more values than are on the stack.

2. **Type Confusion**: Performing operations on values of the wrong type.

3. **Infinite Loops**: Not providing a proper exit condition in loops.

4. **Forgetting Return**: Not using `return` in functions, which can lead to unexpected stack behavior.

## Conclusion

Backstack is a simple yet powerful language with a focus on clarity and expressiveness. While it follows stack-based principles, its readable syntax and comprehensive feature set make it accessible for various programming tasks.

For more examples, check the `examples/` directory in the Backstack repository.
