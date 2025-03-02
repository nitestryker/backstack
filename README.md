
# Backstack Programming Language

Backstack is a stack-based programming language with a simple, readable syntax inspired by Forth. It offers:

- **Stack-Based Execution**: Operations manipulate values on a stack
- **String Manipulation**: Robust string operations including concatenation, slicing, and splitting
- **Variable Support**: Easy-to-use variable definition and access
- **Control Flow**: Conditionals (if/else) and loops (while/for)
- **Functions**: Define and call functions with support for recursion
- **Array Operations**: Create and manipulate array data structures
- **File I/O**: Read from and write to files
- **Bitwise Operations**: Support for bitwise AND, OR, XOR, NOT, and shifts

Backstack programs can be both interpreted (via the `sim` command) or compiled to assembly. The language is designed to be simple to learn yet powerful enough for diverse programming tasks.

## Documentation

For comprehensive documentation on how to program in Backstack, please see [DOCS.md](DOCS.md).

## Examples

```
# Hello World
"Hello, World!"
dump

# Simple calculation
5 3 + dump  # Outputs: 8

# Using variables
10 set:x
20 set:y
get:x get:y + dump  # Outputs: 30

# Defining a function
fun:factorial
  dup 1 <= 
  if 
    drop 1 return
  else
    dup 1 - call:factorial * return
  endif
fun_end

5 call:factorial dump  # Outputs: 120
```
