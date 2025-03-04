
# Function Support in Backstack

The Backstack language now supports function definitions and calls in the assembly code generator. This document describes how functions work in Backstack and how they are implemented in the assembly generator.

## Function Definitions

Functions in Backstack are defined using the `fun:name` and `fun_end` syntax:

```
fun:function_name
  # Function body
  return
fun_end
```

When compiled to assembly, each function is translated into a labeled section of code with proper prologue and epilogue to manage the stack frame. The function name is used to generate a unique label in the assembly code.

## Function Calls

To call a function, use `call:name`:

```
call:function_name
```

This will push the current position onto the call stack and jump to the function's code. When the function returns, execution continues from the point after the call.

## Return Values

Functions in Backstack return the value at the top of the stack when the `return` keyword is encountered. This value is pushed onto the stack at the call site so it can be used in further calculations.

## Example: Factorial Function

Here's an example of a recursive factorial function:

```
fun:factorial
  dup 1 <= if
    drop 1 return  # Base case: return 1
  else
    dup 1 - call:factorial * return  # Recursive case
  endif
fun_end

5 call:factorial dump  # Calculate and print 5! (120)
```

In this example:
1. We define a function named `factorial`
2. We check if the input is less than or equal to 1
3. If it is, we return 1
4. Otherwise, we call `factorial` with the input - 1, and multiply the result by the input

## Assembly Implementation

The assembly code generated for functions handles:

1. Function prologue to set up the stack frame
2. Parameter passing via the stack
3. Return value handling
4. Function epilogue to restore the stack frame
5. Function calls with proper return address handling

The implementation follows standard x86-64 calling conventions, ensuring that registers are properly saved and restored.

## Recursive Functions

Backstack supports recursive functions, as shown in the factorial example. The implementation properly handles the call stack, allowing functions to call themselves without issues.
