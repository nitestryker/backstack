import sys
import subprocess
import os

iota_counter = 0

def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

# Operation codes
OP_PUSH = iota(True)
OP_PUSH_STR = iota()  # New operation for string literals
OP_PLUS = iota()
OP_MINUS = iota()

# Operation types
OP_PUSH = 0
OP_PLUS = 1
OP_MINUS = 2
OP_MULTIPLY = 3
OP_DIVIDE = 4
OP_MODULO = 5
OP_DUMP = 6
OP_SET_VAR = 7
OP_GET_VAR = 8
OP_IF = 9
OP_WHILE = 10
OP_EQUALS = 11
OP_NOT_EQUALS = 12
OP_GREATER_THAN = 13
OP_LESS_THAN = 14
OP_AND = 15
OP_OR = 16
OP_NOT = 17
OP_BITWISE_AND = 18
OP_BITWISE_OR = 19
OP_BITWISE_XOR = 20
OP_BITWISE_NOT = 21

OP_MULTI = iota()
OP_DIVIDE = iota()
OP_MOD = iota()
OP_EXPO = iota()
OP_FLOOR = iota()
# Bitwise operations
OP_BIT_AND = iota()
OP_BIT_OR = iota()
OP_BIT_XOR = iota()
OP_BIT_NOT = iota()
OP_BIT_SHIFT_LEFT = iota()
OP_BIT_SHIFT_RIGHT = iota()
# Comparison operations
OP_EQUAL = iota()
OP_NOT_EQUAL = iota()
OP_GREATER = iota()
OP_LESS = iota()
OP_LESS_EQUAL = iota()
# Conditional operations
OP_IF = iota()
OP_ELSE = iota()
OP_ENDIF = iota()
# Loop operations
OP_WHILE = iota()
OP_REPEAT = iota()
OP_FOR = iota()
OP_NEXT = iota()
# Stack manipulation operations
OP_DUP = iota()
OP_SWAP = iota()
OP_DROP = iota()
OP_OVER = iota()
OP_ROT = iota()
OP_DUMP = iota()
# Variable operations
OP_SET = iota()
OP_GET = iota()
# Memory operations
OP_ARRAY_NEW = iota()
OP_ARRAY_SET = iota()
OP_ARRAY_GET = iota()
OP_ARRAY_LEN = iota()

# String operations
OP_STR_CONCAT = iota()    # String concatenation
OP_STR_LENGTH = iota()    # Get string length
OP_STR_SLICE = iota()     # Get substring
OP_STR_CONTAINS = iota()  # Check if string contains substring
OP_STR_SPLIT = iota()     # Split string by delimiter
OP_STR = iota()           # Convert number to string

# Input operation
OP_INPUT = iota()         # Read input from user
OP_INPUT_INT = iota()     # Read input and convert to integer

# File I/O operations
OP_FILE_OPEN = iota()     # Open a file
OP_FILE_CLOSE = iota()    # Close a file
OP_FILE_READ = iota()     # Read from a file
OP_FILE_WRITE = iota()    # Write to a file
OP_FILE_APPEND = iota()   # Append to a file

# Function operations
OP_FUN_DEF = iota()       # Define a function
OP_FUN_END = iota()       # End function definition
OP_FUN_CALL = iota()      # Call a function
OP_RETURN = iota()        # Return from a function

COUNT_OPS = iota()

# Operation constructors
def push(x):
    return (OP_PUSH, x)

def plus():
    return (OP_PLUS, )

def minus():
    return (OP_MINUS, )

def multi():
    return (OP_MULTI, )

def divide():
    return (OP_DIVIDE, )

def mod():
    return (OP_MOD, )

def expo():
    return (OP_EXPO, )

def floor():
    return (OP_FLOOR, )

# Bitwise operations
def bit_and():
    return (OP_BIT_AND, )

def bit_or():
    return (OP_BIT_OR, )

def bit_xor():
    return (OP_BIT_XOR, )

def bit_not():
    return (OP_BIT_NOT, )

def bit_shift_left():
    return (OP_BIT_SHIFT_LEFT, )

def bit_shift_right():
    return (OP_BIT_SHIFT_RIGHT, )

# Comparison operations
def equal():
    return (OP_EQUAL, )

def not_equal():
    return (OP_NOT_EQUAL, )

def greater():
    return (OP_GREATER, )

def less():
    return (OP_LESS, )
    
def less_equal():
    return (OP_LESS_EQUAL, )

# Conditional operations
def if_op():
    return (OP_IF, )

def else_op():
    return (OP_ELSE, )

def endif():
    return (OP_ENDIF, )

# Loop operations
def while_op():
    return (OP_WHILE, )

def repeat_op():
    return (OP_REPEAT, )

def for_op():
    return (OP_FOR, )

def next_op():
    return (OP_NEXT, )

# Stack manipulation operations
def dup():
    return (OP_DUP, )

def swap():
    return (OP_SWAP, )

def drop():
    return (OP_DROP, )

def over():
    return (OP_OVER, )

def rot():
    return (OP_ROT, )

def dump():
    return (OP_DUMP, )

# Variable operations
def set_var(name):
    return (OP_SET, name)

def get_var(name):
    return (OP_GET, name)

# Memory operations
def array_new():
    return (OP_ARRAY_NEW, )

def array_set():
    return (OP_ARRAY_SET, )

def array_get():
    return (OP_ARRAY_GET, )

def array_len():
    return (OP_ARRAY_LEN, )

# String operations
def push_str(s):
    return (OP_PUSH_STR, s)

def str_concat():
    return (OP_STR_CONCAT, )

def str_length():
    return (OP_STR_LENGTH, )

def str_slice():
    return (OP_STR_SLICE, )

def str_contains():
    return (OP_STR_CONTAINS, )
    
def str_split():
    return (OP_STR_SPLIT, )
    
def str_convert():
    return (OP_STR, )

# Input operations
def input_op():
    return (OP_INPUT, )

def input_int():
    return (OP_INPUT_INT, )
    
# File I/O operations
def file_open():
    return (OP_FILE_OPEN, )
    
def file_close():
    return (OP_FILE_CLOSE, )
    
def file_read():
    return (OP_FILE_READ, )
    
def file_write():
    return (OP_FILE_WRITE, )
    
def file_append():
    return (OP_FILE_APPEND, )
    
# Function operations
def fun_def(name):
    return (OP_FUN_DEF, name)
    
def fun_end():
    return (OP_FUN_END, )
    
def fun_call(name):
    return (OP_FUN_CALL, name)
    
def return_op():
    return (OP_RETURN, )

def simulate_program(program, debug=False):
    stack = []
    variables = {}  # Dictionary to store named variables
    arrays = {}     # Dictionary to store arrays/memory blocks
    files = {}      # Dictionary to store file handles
    functions = {}  # Dictionary to store function definitions
    pc = 0  # Program counter
    skip_mode = False  # For handling conditional branches
    if_stack = []  # Stack to track nested if statements
    loop_stack = []  # Stack to track loop start positions
    call_stack = []  # Stack to track function calls (return addresses)
    
    # First pass: pre-process all function definitions
    if debug:
        print("DEBUG: Pre-processing function definitions...")
    temp_pc = 0
    while temp_pc < len(program):
        op = program[temp_pc]
        if op[0] == OP_FUN_DEF:
            fun_name = op[1]
            functions[fun_name] = temp_pc + 1  # Store position after FUN_DEF
            if debug:
                print(f"DEBUG: Pre-registered function '{fun_name}' at position {temp_pc + 1}")
            
            # Skip the function body (to find the matching FUN_END)
            nesting = 1
            inner_pc = temp_pc + 1
            while inner_pc < len(program):
                if program[inner_pc][0] == OP_FUN_DEF:
                    nesting += 1
                elif program[inner_pc][0] == OP_FUN_END:
                    nesting -= 1
                    if nesting == 0:
                        break
                inner_pc += 1
            
            if inner_pc >= len(program):
                print(f"ERROR: Missing FUN_END for function '{fun_name}'")
                return
                
            temp_pc = inner_pc  # Skip to after FUN_END
        
        temp_pc += 1
    
    if debug:
        print(f"DEBUG: All available functions after pre-processing: {list(functions.keys())}")
    
    # Second pass: execute the program
    while pc < len(program):
        op = program[pc]
        
        # Handle IF/ELSE/ENDIF when in skip mode
        if skip_mode:
            if op[0] == OP_IF:
                if_stack.append(False)  # Track nested if when skipping
            elif op[0] == OP_ELSE:
                if len(if_stack) > 0 and if_stack[-1] is False:
                    skip_mode = False  # Exit skip mode at matching else
                    if_stack.pop()
            elif op[0] == OP_ENDIF:
                if len(if_stack) > 0:
                    if_stack.pop()  # Pop nested if
                else:
                    skip_mode = False  # Exit skip mode at endif
            
            pc += 1
            continue
            
        # Normal operation execution
        if op[0] == OP_PUSH:
            stack.append(op[1])
        elif op[0] == OP_PLUS:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for addition")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(a + b)
        elif op[0] == OP_MINUS:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for subtraction")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(b - a)
        elif op[0] == OP_MULTI:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for multiplication")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(a * b)
        elif op[0] == OP_DIVIDE:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for division")
                return
            a, b = stack.pop(), stack.pop()
            if a == 0:
                print("ERROR: Division by zero")
                return
            stack.append(b / a)  # Note: This does floating-point division
        elif op[0] == OP_MOD:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for modulo")
                return
            a, b = stack.pop(), stack.pop()
            if a == 0:
                print("ERROR: Modulo by zero")
                return
            stack.append(b % a)
        elif op[0] == OP_EXPO:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for exponentiation")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(b ** a)
        elif op[0] == OP_FLOOR:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for floor division")
                return
            a, b = stack.pop(), stack.pop()
            if a == 0:
                print("ERROR: Floor division by zero")
                return
            stack.append(b // a)
            
        # Bitwise operations
        elif op[0] == OP_BIT_AND:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for bitwise AND")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(b & a)
        elif op[0] == OP_BIT_OR:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for bitwise OR")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(b | a)
        elif op[0] == OP_BIT_XOR:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for bitwise XOR")
                return
            a, b = stack.pop(), stack.pop()
            # Ensure both operands are converted to integers before operation
            a_int = int(a) if not isinstance(a, bool) else int(a)
            b_int = int(b) if not isinstance(b, bool) else int(b)
            # Perform bitwise XOR operation
            result = b_int ^ a_int
            stack.append(result)
        elif op[0] == OP_BIT_NOT:
            if not stack:
                print("ERROR: Stack is empty, cannot perform bitwise NOT")
                return
            a = stack.pop()
            stack.append(~a)
        elif op[0] == OP_BIT_SHIFT_LEFT:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for bitwise shift left")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(b << a)
        elif op[0] == OP_BIT_SHIFT_RIGHT:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for bitwise shift right")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(b >> a)
            
        # Comparison operations
        elif op[0] == OP_EQUAL:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for comparison")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(1 if b == a else 0)  # Push 1 for true, 0 for false
        elif op[0] == OP_NOT_EQUAL:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for comparison")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(1 if b != a else 0)
        elif op[0] == OP_GREATER:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for comparison")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(1 if b > a else 0)
        elif op[0] == OP_LESS:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for comparison")
                return
            a, b = stack.pop(), stack.pop()
            stack.append(1 if b < a else 0)
            
        elif op[0] == OP_LESS_EQUAL:
            if len(stack) < 2:
                print("ERROR: Not enough values in stack for comparison")
                return
            a, b = stack.pop(), stack.pop()
            result = 1 if b <= a else 0
            if debug:
                print(f"DEBUG: Less than or equal: {b} <= {a} = {result}")
            stack.append(result)
            
        # Conditional operations
        elif op[0] == OP_IF:
            if not stack:
                print("ERROR: Stack is empty, cannot evaluate condition")
                return
            condition = stack.pop()
            if condition == 0:  # If false (0)
                skip_mode = True
                if_stack.append(True)  # Mark this if as the active one
            else:
                if_stack.append(False)  # Not skipping but track for nested ifs
        elif op[0] == OP_ELSE:
            if len(if_stack) == 0:
                print("ERROR: ELSE without matching IF")
                return
            if if_stack[-1] is False:  # We didn't skip the IF part
                skip_mode = True  # Skip the ELSE part
            if_stack.pop()  # Pop the current if
            if_stack.append(not skip_mode)  # Track for nested if
        elif op[0] == OP_ENDIF:
            if len(if_stack) == 0:
                print("ERROR: ENDIF without matching IF")
                return
            if_stack.pop()  # Clear current if state
            
        # Stack manipulation operations
        elif op[0] == OP_DUP:
            if not stack:
                print("ERROR: Stack is empty, cannot duplicate")
                return
            stack.append(stack[-1])  # Duplicate the top item
        elif op[0] == OP_SWAP:
            if len(stack) < 2:
                print("ERROR: Need at least two values to swap")
                return
            stack[-1], stack[-2] = stack[-2], stack[-1]  # Swap top two items
        elif op[0] == OP_DROP:
            if not stack:
                print("ERROR: Stack is empty, cannot drop")
                return
            stack.pop()  # Remove the top item
        elif op[0] == OP_OVER:
            if len(stack) < 2:
                print("ERROR: Need at least two values for OVER")
                return
            stack.append(stack[-2])  # Copy the second item to the top
        elif op[0] == OP_ROT:
            if len(stack) < 3:
                print("ERROR: Need at least three values for ROT")
                return
            # Rotate the top three items: (a b c -- b c a)
            a, b, c = stack.pop(), stack.pop(), stack.pop()
            stack.extend([b, a, c])
            
        elif op[0] == OP_DUMP:
            if not stack:
                print("ERROR: Stack is empty, nothing to dump")
                return
            print(stack.pop())
            
        # Loop operations
        elif op[0] == OP_WHILE:
            # Mark the start of a while loop
            loop_stack.append(pc)
            
        elif op[0] == OP_REPEAT:
            if not stack:
                print("ERROR: Stack is empty, cannot evaluate loop condition")
                return
            condition = stack.pop()
            if condition != 0:  # If condition is true (non-zero)
                # Jump back to the matching WHILE
                if not loop_stack:
                    print("ERROR: REPEAT without matching WHILE")
                    return
                pc = loop_stack[-1]
            else:
                # Exit the loop
                loop_stack.pop()
                
        elif op[0] == OP_FOR:
            # FOR expects: end_value start_value
            if len(stack) < 2:
                print("ERROR: Not enough values for FOR loop")
                return
            start_value = stack.pop()
            end_value = stack.pop()
            
            # Store loop counter in a special variable
            variables["_loop_counter"] = start_value
            
            # Store loop end condition
            variables["_loop_end"] = end_value
            
            # Mark loop start for NEXT to jump back to
            loop_stack.append(pc)
            
            # Push the current counter value back to the stack
            stack.append(start_value)
            
        elif op[0] == OP_NEXT:
            if "_loop_counter" not in variables or "_loop_end" not in variables:
                print("ERROR: NEXT without proper FOR setup")
                return
            
            # Increment loop counter
            variables["_loop_counter"] += 1
            
            # Check if we should continue looping
            if variables["_loop_counter"] <= variables["_loop_end"]:
                # Push current counter to stack
                stack.append(variables["_loop_counter"])
                
                # Jump back to the matching FOR
                if not loop_stack:
                    print("ERROR: NEXT without matching FOR")
                    return
                pc = loop_stack[-1]
            else:
                # Exit the loop
                loop_stack.pop()
                del variables["_loop_counter"]
                del variables["_loop_end"]
            
        # Variable operations
        elif op[0] == OP_SET:
            if not stack:
                print(f"ERROR: Stack is empty, cannot set variable '{op[1]}'")
                return
            variables[op[1]] = stack.pop()
        elif op[0] == OP_GET:
            if op[1] not in variables:
                print(f"ERROR: Variable '{op[1]}' is not defined")
                return
            stack.append(variables[op[1]])
            
        # Memory/Array operations
        elif op[0] == OP_ARRAY_NEW:
            if not stack:
                print("ERROR: Stack is empty, cannot create array")
                return
            size = stack.pop()
            if size < 0:
                print("ERROR: Array size cannot be negative")
                return
            array_id = len(arrays)
            arrays[array_id] = [0] * size
            stack.append(array_id)
        elif op[0] == OP_ARRAY_SET:
            if len(stack) < 3:
                print("ERROR: Not enough values for array set operation")
                return
            value = stack.pop()
            index = stack.pop()
            array_id = stack.pop()
            if array_id not in arrays:
                print(f"ERROR: Array {array_id} does not exist")
                return
            if index < 0 or index >= len(arrays[array_id]):
                print(f"ERROR: Index {index} out of bounds for array {array_id}")
                return
            arrays[array_id][index] = value
        elif op[0] == OP_ARRAY_GET:
            if len(stack) < 2:
                print("ERROR: Not enough values for array get operation")
                return
            index = stack.pop()
            array_id = stack.pop()
            if array_id not in arrays:
                print(f"ERROR: Array {array_id} does not exist")
                return
            if index < 0 or index >= len(arrays[array_id]):
                print(f"ERROR: Index {index} out of bounds for array {array_id}")
                return
            stack.append(arrays[array_id][index])
        elif op[0] == OP_ARRAY_LEN:
            if not stack:
                print("ERROR: Stack is empty, cannot get array length")
                return
            array_id = stack.pop()
            if array_id not in arrays:
                print(f"ERROR: Array {array_id} does not exist")
                return
            stack.append(len(arrays[array_id]))
            
        # String operations
        elif op[0] == OP_PUSH_STR:
            stack.append(op[1])  # Push string literal to stack
        elif op[0] == OP_STR_CONCAT:
            if len(stack) < 2:
                print("ERROR: Not enough values for string concatenation")
                return
            str2 = stack.pop()
            str1 = stack.pop()
            if not isinstance(str1, str) or not isinstance(str2, str):
                print("ERROR: String concatenation requires two strings")
                return
            stack.append(str1 + str2)
        elif op[0] == OP_STR_LENGTH:
            if not stack:
                print("ERROR: Stack is empty, cannot get string length")
                return
            s = stack.pop()
            if not isinstance(s, str):
                print("ERROR: String length operation requires a string")
                return
            stack.append(len(s))
        elif op[0] == OP_STR_SLICE:
            if len(stack) < 3:
                print("ERROR: Not enough values for string slice")
                return
            end = stack.pop()
            start = stack.pop()
            s = stack.pop()
            if not isinstance(s, str):
                print("ERROR: String slice operation requires a string")
                return
            try:
                stack.append(s[start:end])
            except (IndexError, TypeError):
                print(f"ERROR: Invalid string slice indices: {start}:{end}")
                return
        elif op[0] == OP_STR_CONTAINS:
            if len(stack) < 2:
                print("ERROR: Not enough values for string contains")
                return
            substring = stack.pop()
            s = stack.pop()
            if not isinstance(s, str) or not isinstance(substring, str):
                print("ERROR: String contains operation requires two strings")
                return
            stack.append(1 if substring in s else 0)  # 1 for true, 0 for false
            
        elif op[0] == OP_STR_SPLIT:
            if len(stack) < 2:
                print("ERROR: Not enough values for string split")
                return
            delimiter = stack.pop()
            s = stack.pop()
            if not isinstance(s, str) or not isinstance(delimiter, str):
                print("ERROR: String split operation requires two strings")
                return
            result = s.split(delimiter)
            array_id = len(arrays)
            arrays[array_id] = result
            stack.append(array_id)
            
        elif op[0] == OP_STR:
            if len(stack) < 1:
                print("ERROR: Not enough values for string conversion")
                return
            value = stack.pop()
            stack.append(str(value))
        
        # Input operations
        elif op[0] == OP_INPUT:
            # Get input prompt if available
            prompt = ""
            if stack:
                prompt_value = stack.pop()
                if isinstance(prompt_value, str):
                    prompt = prompt_value
                else:
                    # Push it back if it's not a string
                    stack.append(prompt_value)
            
            # Read input from user
            user_input = input(prompt)
            stack.append(user_input)
            
        elif op[0] == OP_INPUT_INT:
            # Get input prompt if available
            prompt = ""
            if stack:
                prompt_value = stack.pop()
                if isinstance(prompt_value, str):
                    prompt = prompt_value
                else:
                    # Push it back if it's not a string
                    stack.append(prompt_value)
                    
            # Read input and convert to integer
            try:
                user_input = int(input(prompt))
                stack.append(user_input)
            except ValueError:
                print("ERROR: Input could not be converted to integer")
                return
                
        # File I/O operations
        elif op[0] == OP_FILE_OPEN:
            if len(stack) < 2:
                print("ERROR: Need filename and mode to open file")
                return
            mode = stack.pop()  # Mode: 'r' for read, 'w' for write
            filename = stack.pop()
            
            if not isinstance(filename, str) or not isinstance(mode, str):
                print("ERROR: Filename and mode must be strings")
                return
                
            try:
                file_handle = len(files)  # Use the length as a unique handle
                files[file_handle] = open(filename, mode)
                stack.append(file_handle)  # Return the file handle
            except Exception as e:
                print(f"ERROR: Could not open file: {e}")
                return
                
        elif op[0] == OP_FILE_CLOSE:
            if not stack:
                print("ERROR: Need file handle to close file")
                return
            file_handle = stack.pop()
            
            if file_handle not in files:
                print(f"ERROR: Invalid file handle: {file_handle}")
                return
                
            try:
                files[file_handle].close()
                del files[file_handle]  # Remove from our dictionary
            except Exception as e:
                print(f"ERROR: Could not close file: {e}")
                return
                
        elif op[0] == OP_FILE_READ:
            if not stack:
                print("ERROR: Need file handle to read from file")
                return
            file_handle = stack.pop()
            
            if file_handle not in files:
                print(f"ERROR: Invalid file handle: {file_handle}")
                return
                
            try:
                content = files[file_handle].read()
                stack.append(content)
            except Exception as e:
                print(f"ERROR: Could not read from file: {e}")
                return
                
        elif op[0] == OP_FILE_WRITE:
            if len(stack) < 2:
                print("ERROR: Need file handle and content to write to file")
                return
            content = stack.pop()
            file_handle = stack.pop()
            
            if file_handle not in files:
                print(f"ERROR: Invalid file handle: {file_handle}")
                return
                
            try:
                files[file_handle].write(str(content))  # Convert to string in case content is not a string
                files[file_handle].flush()  # Ensure it's written to disk
            except Exception as e:
                print(f"ERROR: Could not write to file: {e}")
                return
                
        elif op[0] == OP_FILE_APPEND:
            if len(stack) < 2:
                print("ERROR: Need file handle and content to append to file")
                return
            content = stack.pop()
            file_handle = stack.pop()
            
            if file_handle not in files:
                print(f"ERROR: Invalid file handle: {file_handle}")
                return
            
            # Make sure file is in append mode
            if files[file_handle].mode not in ('a', 'a+'):
                print(f"ERROR: File not opened in append mode")
                return
                
            try:
                files[file_handle].write(str(content))
                files[file_handle].flush()  # Ensure it's written to disk
            except Exception as e:
                print(f"ERROR: Could not append to file: {e}")
                return
                
        # Function operations
        elif op[0] == OP_FUN_DEF:
            # Function was already defined in pre-processing, just skip to matching FUN_END
            fun_name = op[1]
            if debug:
                    print(f"DEBUG: Skipping already defined function '{fun_name}' body")
            
            # Skip to matching FUN_END
            nesting = 1
            temp_pc = pc + 1
            while temp_pc < len(program):
                if program[temp_pc][0] == OP_FUN_DEF:
                    nesting += 1
                elif program[temp_pc][0] == OP_FUN_END:
                    nesting -= 1
                    if nesting == 0:
                        break
                temp_pc += 1
                
            if temp_pc >= len(program):
                print(f"ERROR: Missing FUN_END for function '{fun_name}'")
                return
                
            pc = temp_pc  # Skip to after the FUN_END
                
        elif op[0] == OP_FUN_END:
            # Return from function if in a function call
            if call_stack:
                pc = call_stack.pop()  # Return to caller
            else:
                # If not in a function call, this is the end of a function definition
                # which we already skip over during definition
                pass
                
        elif op[0] == OP_FUN_CALL:
            fun_name = op[1]
            if debug:
                print(f"DEBUG: Calling function '{fun_name}', available functions: {list(functions.keys())}")
            if fun_name not in functions:
                print(f"ERROR: Function '{fun_name}' is not defined")
                return
                
            # Save current position to return to
            call_stack.append(pc)
            
            # Jump to function
            pc = functions[fun_name]
            if debug:
                print(f"DEBUG: Jumped to function position {pc}")
            continue  # Skip pc increment
            
        elif op[0] == OP_RETURN:
            # Return from function
            if call_stack:
                pc = call_stack.pop()  # Return to caller
            else:
                print("ERROR: RETURN outside of function")
                return
                
        else:
            assert False, f"Unreachable: op code {op[0]}"
            
        pc += 1

def compile_program(program, out_file_path):
    with open(out_file_path, "w") as out:
        # We'll collect data section entries as we go
        data_section = []
        data_section.append('fmt db "%d", 10, 0')
        
        out.write("extern printf\n")
        out.write("extern ExitProcess\n")
        out.write("extern fflush\n")  # Include fflush
        out.write("extern __acrt_iob_func\n")  # Windows function for stdout

        # For tracking variables and arrays in the data section
        compiler_data = {}
        
        # For generating unique labels
        label_counter = 0
        array_counter = 0
        if_stack = []

        for op in program:
            if op[0] == OP_PUSH:
                out.write(f"  push {op[1]}\n")
            elif op[0] == OP_PLUS:
                out.write("  pop rax\n  pop rbx\n  add rax, rbx\n  push rax\n")
            elif op[0] == OP_MINUS:
                out.write("  pop rax\n  pop rbx\n  sub rbx, rax\n  push rbx\n")
            elif op[0] == OP_MULTI:
                out.write("  pop rax\n  pop rbx\n  imul rax, rbx\n  push rax\n")
            elif op[0] == OP_DIVIDE:
                # x86 division is a bit complex - uses rdx:rax / operand
                out.write("  pop rbx\n")           # Divisor in rbx
                out.write("  pop rax\n")           # Dividend in rax
                out.write("  xor rdx, rdx\n")      # Clear rdx for division
                out.write("  div rbx\n")           # rdx:rax / rbx, quotient in rax
                out.write("  push rax\n")          # Push quotient
            elif op[0] == OP_MOD:
                # Modulo uses remainder from division
                out.write("  pop rbx\n")           # Divisor in rbx
                out.write("  pop rax\n")           # Dividend in rax
                out.write("  xor rdx, rdx\n")      # Clear rdx for division
                out.write("  div rbx\n")           # rdx:rax / rbx, remainder in rdx
                out.write("  push rdx\n")          # Push remainder
            elif op[0] == OP_EXPO:
                # For exponentiation, we'll need a simple loop
                out.write("  pop rbx\n")           # Exponent in rbx
                out.write("  pop rax\n")           # Base in rax
                out.write("  mov rcx, 1\n")        # Initialize result to 1
                out.write("  cmp rbx, 0\n")        # Check if exponent is 0
                out.write("  je .expo_done\n")     # If zero, result is already 1
                out.write(".expo_loop:\n")
                out.write("  imul rcx, rax\n")     # Multiply result by base
                out.write("  dec rbx\n")           # Decrement exponent counter
                out.write("  jnz .expo_loop\n")    # Continue if exponent not zero
                out.write(".expo_done:\n")
                out.write("  push rcx\n")          # Push final result
            elif op[0] == OP_FLOOR:
                # Floor division is the same as integer division in assembly
                out.write("  pop rbx\n")           # Divisor in rbx
                out.write("  pop rax\n")           # Dividend in rax
                out.write("  xor rdx, rdx\n")      # Clear rdx for division
                out.write("  div rbx\n")           # rdx:rax / rbx, quotient in rax
                out.write("  push rax\n")          # Push quotient
                
            # Comparison operations
            elif op[0] == OP_EQUAL:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  xor rcx, rcx\n")  # Clear rcx (will store result)
                out.write("  cmp rbx, rax\n")  # Compare values
                out.write("  sete cl\n")       # Set cl to 1 if equal, 0 if not
                out.write("  push rcx\n")      # Push result
            elif op[0] == OP_NOT_EQUAL:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  xor rcx, rcx\n")
                out.write("  cmp rbx, rax\n")
                out.write("  setne cl\n")      # Set cl to 1 if not equal
                out.write("  push rcx\n")
            elif op[0] == OP_GREATER:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  xor rcx, rcx\n")
                out.write("  cmp rbx, rax\n")
                out.write("  setg cl\n")       # Set cl to 1 if greater
                out.write("  push rcx\n")
            elif op[0] == OP_LESS:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  xor rcx, rcx\n")
                out.write("  cmp rbx, rax\n")
                out.write("  setl cl\n")       # Set cl to 1 if less
                out.write("  push rcx\n")
            elif op[0] == OP_LESS_EQUAL:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  xor rcx, rcx\n")
                out.write("  cmp rbx, rax\n")
                out.write("  setle cl\n")      # Set cl to 1 if less or equal
                out.write("  push rcx\n")
                
            # Conditional operations
            elif op[0] == OP_IF:
                label_counter += 1
                else_label = f".else_{label_counter}"
                endif_label = f".endif_{label_counter}"
                
                out.write("  pop rax\n")
                out.write("  cmp rax, 0\n")
                out.write(f"  je {else_label}\n")  # Jump to else if condition is false
                
                # Push labels onto stack for nested if handling
                if_stack.append((else_label, endif_label))
                
            elif op[0] == OP_ELSE:
                if not if_stack:
                    raise ValueError("ELSE without matching IF")
                    
                else_label, endif_label = if_stack.pop()
                out.write(f"  jmp {endif_label}\n")  # Jump over else section
                out.write(f"{else_label}:\n")  # Else label
                
                # Push just the endif label back for the matching ENDIF
                if_stack.append((None, endif_label))
                
            elif op[0] == OP_ENDIF:
                if not if_stack:
                    raise ValueError("ENDIF without matching IF")
                    
                else_or_none, endif_label = if_stack.pop()
                
                # If there was no ELSE, we need to define the else label here
                if else_or_none is not None:
                    out.write(f"{else_or_none}:\n")
                    
                out.write(f"{endif_label}:\n")  # Endif label
                
            # Stack manipulation operations
            elif op[0] == OP_DUP:
                out.write("  pop rax\n")
                out.write("  push rax\n")
                out.write("  push rax\n")
            elif op[0] == OP_SWAP:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  push rax\n")
                out.write("  push rbx\n")
            elif op[0] == OP_DROP:
                out.write("  pop rax\n")  # Just pop and discard
            elif op[0] == OP_OVER:
                out.write("  pop rax\n")
                out.write("  pop rbx\n")
                out.write("  push rbx\n")
                out.write("  push rax\n")
                out.write("  push rbx\n")
            elif op[0] == OP_ROT:
                out.write("  pop rax\n")  # Top item (c)
                out.write("  pop rbx\n")  # Middle item (b)
                out.write("  pop rcx\n")  # Bottom item (a)
                out.write("  push rbx\n") # New bottom: b
                out.write("  push rax\n") # New middle: c
                out.write("  push rcx\n") # New top: a
                
            elif op[0] == OP_DUMP:
                out.write("  sub rsp, 32\n")  # Stack alignment
                out.write("  pop rcx\n")  # First argument: integer to print
                out.write("  mov rdx, fmt\n")  # Second argument: format string
                out.write("  xor rax, rax\n")  # Windows x64 ABI: RAX = 0 before printf
                out.write("  call printf\n")  # Call printf
                out.write("  mov rcx, 1\n")  # Argument for __acrt_iob_func (1 = stdout)
                out.write("  call __acrt_iob_func\n")  # Get stdout
                out.write("  mov rcx, rax\n")  # Pass stdout to fflush
                out.write("  call fflush\n")  # Flush stdout
                out.write("  add rsp, 32\n")  # Restore stack
                out.write("  mov ecx, 0\n")  # Exit code 0
                out.write("  call ExitProcess\n")  # Exit program
                
            # Variable operations - for assembly we'll use memory locations with variable names as labels
            elif op[0] == OP_SET:
                var_name = f"var_{op[1]}"
                # Make sure the variable is defined in data section
                if var_name not in compiler_data:
                    compiler_data[var_name] = True
                    data_section.append(f"{var_name} dq 0")
                out.write("  pop rax\n")
                out.write(f"  mov [rel {var_name}], rax\n")
            elif op[0] == OP_GET:
                var_name = f"var_{op[1]}"
                # Make sure the variable is defined in data section
                if var_name not in compiler_data:
                    compiler_data[var_name] = True
                    data_section.append(f"{var_name} dq 0")
                out.write(f"  mov rax, [rel {var_name}]\n")
                out.write("  push rax\n")
                
            # Array operations - we'll use a simple memory allocation scheme
            elif op[0] == OP_ARRAY_NEW:
                out.write("  pop rax\n")  # Get size
                out.write("  imul rax, 8\n")  # Multiply by 8 bytes per element
                # For simplicity in this example, we'll just use a static array
                # A real implementation would use memory allocation
                array_label = f"array_{array_counter}"
                array_counter += 1
                if array_label not in compiler_data:
                    compiler_data[array_label] = True
                    data_section.append(f"{array_label} times 1000 dq 0")  # Fixed size array
                out.write(f"  mov rax, {array_counter-1}\n")  # Return array ID
                out.write("  push rax\n")
            elif op[0] == OP_ARRAY_SET:
                out.write("  pop rcx\n")  # Value
                out.write("  pop rbx\n")  # Index
                out.write("  pop rax\n")  # Array ID
                # Simple array access, no bounds checking in assembly
                out.write("  imul rbx, 8\n")  # Multiply index by 8 bytes
                out.write(f"  lea rdx, [rel array_0]\n")  # Base array address
                out.write("  imul rax, 1000*8\n")  # Offset for array ID
                out.write("  add rdx, rax\n")  # Add array offset
                out.write("  add rdx, rbx\n")  # Add index offset
                out.write("  mov [rdx], rcx\n")  # Store value
            elif op[0] == OP_ARRAY_GET:
                out.write("  pop rbx\n")  # Index
                out.write("  pop rax\n")  # Array ID
                out.write("  imul rbx, 8\n")  # Multiply index by 8 bytes
                out.write(f"  lea rdx, [rel array_0]\n")  # Base array address
                out.write("  imul rax, 1000*8\n")  # Offset for array ID
                out.write("  add rdx, rax\n")  # Add array offset
                out.write("  add rdx, rbx\n")  # Add index offset
                out.write("  mov rcx, [rdx]\n")  # Get value
                out.write("  push rcx\n")  # Push value
            elif op[0] == OP_ARRAY_LEN:
                # Since we're using fixed-size arrays, we'll need to track lengths separately
                # This is a simplification; a real implementation would store lengths with arrays
                out.write("  pop rax\n")  # Array ID
                out.write("  mov rax, 1000\n")  # Fixed size
                out.write("  push rax\n")
            else:
                assert False, f"Unreachable: op code {op[0]}"
                
        # Write the data section after processing all operations
        out.write("section .data\n")
        for data_item in data_section:
            out.write(f"{data_item}\n")
            
        out.write("section .text\n")
        out.write("global _start\n")
        out.write("_start:\n")

def read_program_from_args(args):
    program = []
    if len(args) > 0 and os.path.isfile(args[0]):
        with open(args[0], "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip comments (lines starting with #)
            if line.startswith('#'):
                continue
                
            # Remove inline comments
            if '#' in line:
                line = line.split('#', 1)[0].strip()
                if not line:  # If line is now empty after removing comment
                    continue

            # Check for string literals (enclosed in quotes)
            if (line.startswith('"') and line.endswith('"')) or (line.startswith("'") and line.endswith("'")):
                # Extract string content without quotes
                string_content = line[1:-1]
                program.append(push_str(string_content))
            elif line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                program.append(push(int(line)))
            elif line == "+":
                program.append(plus())
            elif line == "-":
                program.append(minus())
            elif line == "*":
                program.append(multi())
            elif line == "/":
                program.append(divide())
            elif line == "%":
                program.append(mod())
            elif line == "^":
                program.append(expo())
            elif line == "//":
                program.append(floor())
            # Bitwise operations
            elif line == "&":
                program.append(bit_and())
            elif line == "|":
                program.append(bit_or())
            elif line == "^" and len(program) > 0 and program[-1][0] != OP_PUSH:  # Make sure it's not an exponentiation
                program.append(bit_xor())
            elif line == "^":
                program.append(expo())
            elif line == "~":
                program.append(bit_not())
            elif line == "<<":
                program.append(bit_shift_left())
            elif line == ">>":
                program.append(bit_shift_right())
            # Comparison operations
            elif line == "==":
                program.append(equal())
            elif line == "!=":
                program.append(not_equal())
            elif line == ">":
                program.append(greater())
            elif line == "<":
                program.append(less())
            elif line == "<=":
                program.append(less_equal())
            # Conditional operations
            elif line.lower() == "if":
                program.append(if_op())
            elif line.lower() == "else":
                program.append(else_op())
            elif line.lower() == "endif":
                program.append(endif())
            # Loop operations
            elif line.lower() == "while":
                program.append(while_op())
            elif line.lower() == "repeat":
                program.append(repeat_op())
            elif line.lower() == "for":
                program.append(for_op())
            elif line.lower() == "next":
                program.append(next_op())
            # Stack manipulation operations
            elif line.lower() == "dup":
                program.append(dup())
            elif line.lower() == "swap":
                program.append(swap())
            elif line.lower() == "drop":
                program.append(drop())
            elif line.lower() == "over":
                program.append(over())
            elif line.lower() == "rot":
                program.append(rot())
            elif line == "dump":
                program.append(dump())
            # Variable operations
            elif line.startswith("set:"):
                var_name = line[4:]  # Extract variable name
                program.append(set_var(var_name))
            elif line.startswith("get:"):
                var_name = line[4:]  # Extract variable name
                program.append(get_var(var_name))
            # Array operations
            elif line == "array_new":
                program.append(array_new())
            elif line == "array_set":
                program.append(array_set())
            elif line == "array_get":
                program.append(array_get())
            elif line == "array_len":
                program.append(array_len())
            # String operations
            elif line == "str_concat":
                program.append(str_concat())
            elif line == "str_length":
                program.append(str_length())
            elif line == "str_slice":
                program.append(str_slice())
            elif line == "str_contains":
                program.append(str_contains())
            elif line == "str_split":
                program.append(str_split())
            elif line == "str":
                program.append(str_convert())
            elif line == "input":
                program.append(input_op())
            elif line == "input_int":
                program.append(input_int())
            elif line == "file_open":
                program.append(file_open())
            elif line == "file_close":
                program.append(file_close())
            elif line == "file_read":
                program.append(file_read())
            elif line == "file_write":
                program.append(file_write())
            elif line == "file_append":
                program.append(file_append())
            elif line.startswith("fun:"):
                fun_name = line[4:]  # Extract function name
                program.append(fun_def(fun_name))
            elif line == "fun_end":
                program.append(fun_end())
            elif line.startswith("call:"):
                fun_name = line[5:]  # Extract function name
                program.append(fun_call(fun_name))
            elif line == "return":
                program.append(return_op())
            else:
                print(f"ERROR: Unknown operation '{line}'")
                exit(1)
    else:
        for arg in args:
            # Skip comments (args starting with #)
            if arg.startswith('#'):
                continue
                
            # Remove inline comments
            if '#' in arg:
                arg = arg.split('#', 1)[0].strip()
                if not arg:  # If arg is now empty after removing comment
                    continue
                
            if arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit()):
                program.append(push(int(arg)))
            elif arg == "+":
                program.append(plus())
            elif arg == "-":
                program.append(minus())
            elif arg == "*":
                program.append(multi())
            elif arg == "/":
                program.append(divide())
            elif arg == "%":
                program.append(mod())
            elif arg == "^":
                program.append(expo())
            elif arg == "//":
                program.append(floor())
            # Bitwise operations
            elif arg == "&":
                program.append(bit_and())
            elif arg == "|":
                program.append(bit_or())
            elif arg == "^" and len(program) > 0 and program[-1][0] != OP_PUSH:  # Make sure it's not an exponentiation
                program.append(bit_xor())
            elif arg == "^":
                program.append(expo())
            elif arg == "~":
                program.append(bit_not())
            elif arg == "<<":
                program.append(bit_shift_left())
            elif arg == ">>":
                program.append(bit_shift_right())
            # Comparison operations
            elif arg == "==":
                program.append(equal())
            elif arg == "!=":
                program.append(not_equal())
            elif arg == ">":
                program.append(greater())
            elif arg == "<":
                program.append(less())
            elif arg == "<=":
                program.append(less_equal())
            # Conditional operations
            elif arg.lower() == "if":
                program.append(if_op())
            elif arg.lower() == "else":
                program.append(else_op())
            elif arg.lower() == "endif":
                program.append(endif())
            # Loop operations
            elif arg.lower() == "while":
                program.append(while_op())
            elif arg.lower() == "repeat":
                program.append(repeat_op())
            elif arg.lower() == "for":
                program.append(for_op())
            elif arg.lower() == "next":
                program.append(next_op())
            # Stack manipulation operations
            elif arg.lower() == "dup":
                program.append(dup())
            elif arg.lower() == "swap":
                program.append(swap())
            elif arg.lower() == "drop":
                program.append(drop())
            elif arg.lower() == "over":
                program.append(over())
            elif arg.lower() == "rot":
                program.append(rot())
            elif arg == "dump":
                program.append(dump())
            # Variable operations - format: "set:name" or "get:name"
            elif arg.startswith("set:"):
                var_name = arg[4:]  # Extract variable name
                program.append(set_var(var_name))
            elif arg.startswith("get:"):
                var_name = arg[4:]  # Extract variable name
                program.append(get_var(var_name))
            # Array operations
            elif arg == "array_new":
                program.append(array_new())
            elif arg == "array_set":
                program.append(array_set())
            elif arg == "array_get":
                program.append(array_get())
            elif arg == "array_len":
                program.append(array_len())
            # String operations
            elif arg == "str_concat":
                program.append(str_concat())
            elif arg == "str_length":
                program.append(str_length())
            elif arg == "str_slice":
                program.append(str_slice())
            elif arg == "str_contains":
                program.append(str_contains())
            elif arg == "str_split":
                program.append(str_split())
            elif arg == "str":
                program.append(str_convert())
            elif arg == "input":
                program.append(input_op())
            elif arg == "input_int":
                program.append(input_int())
            elif arg == "file_open":
                program.append(file_open())
            elif arg == "file_close":
                program.append(file_close())
            elif arg == "file_read":
                program.append(file_read())
            elif arg == "file_write":
                program.append(file_write())
            elif arg == "file_append":
                program.append(file_append())
            elif arg.startswith("fun:"):
                fun_name = arg[4:]  # Extract function name
                program.append(fun_def(fun_name))
            elif arg == "fun_end":
                program.append(fun_end())
            elif arg.startswith("call:"):
                fun_name = arg[5:]  # Extract function name
                program.append(fun_call(fun_name))
            elif arg == "return":
                program.append(return_op())
            # Check for string literals in command line args
            elif (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                string_content = arg[1:-1]
                program.append(push_str(string_content))
            else:
                print(f"ERROR: Unknown operation '{arg}'")
                exit(1)

    return program

def usage():
    print("Usage: python main.py <SUBCOMMAND> [ARGS]")
    print("SUBCOMMANDS:")
    print("    sim    Simulate the program")
    print("    com    Compile the program")

def call_cmd(cmd):
    print(cmd)
    subprocess.call(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        print("ERROR: No program instructions provided")
        exit(1)

    subcommand = sys.argv[1]
    program = read_program_from_args(sys.argv[2:])

    if subcommand == "sim":
        simulate_program(program)
    elif subcommand == "com":
        compile_program(program, "output.asm")
        call_cmd(["nasm", "-g", "-fwin64", "output.asm", "-o", "output.o"])
        call_cmd(["gcc", "output.o", "-o", "output.exe", "-nostdlib", "-lkernel32", "-lmsvcrt", "-Wl,--subsystem,console", "-Wl,-e,_start"])
    else:
        usage()
        print(f"ERROR: Unknown subcommand '{subcommand}'")
        exit(1)