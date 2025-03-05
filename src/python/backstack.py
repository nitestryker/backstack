
import os
import sys

# Operation codes
OP_PUSH = "PUSH"
OP_PUSH_STR = "PUSH_STR"
OP_PLUS = "PLUS"
OP_MINUS = "MINUS"
OP_MULT = "MULT"
OP_DIV = "DIV"
OP_MOD = "MOD"
OP_AND = "AND"
OP_OR = "OR"
OP_XOR = "XOR"
OP_NOT = "NOT"
OP_EQ = "EQ"
OP_NEQ = "NEQ"
OP_GT = "GT"
OP_LT = "LT"
OP_DUMP = "DUMP"
OP_SET_VAR = "SET_VAR"
OP_GET_VAR = "GET_VAR"
OP_FUNC_DEF = "FUNC_DEF"
OP_FUNC_CALL = "FUNC_CALL"
OP_RETURN = "RETURN"
OP_ARRAY_NEW = "ARRAY_NEW"
OP_ARRAY_SET = "ARRAY_SET"
OP_ARRAY_GET = "ARRAY_GET"
OP_ARRAY_LEN = "ARRAY_LEN"
OP_STR_CONCAT = "STR_CONCAT"
OP_STR_LENGTH = "STR_LENGTH"
OP_STR_SLICE = "STR_SLICE"
OP_STR_CONTAINS = "STR_CONTAINS"
OP_STR_SPLIT = "STR_SPLIT"
OP_STR = "STR"
OP_FILE_OPEN = "FILE_OPEN"
OP_FILE_CLOSE = "FILE_CLOSE"
OP_FILE_READ = "FILE_READ"
OP_FILE_WRITE = "FILE_WRITE"
OP_FILE_APPEND = "FILE_APPEND"

# Helper functions to create operations
def push(value):
    return (OP_PUSH, value)
    
def push_str(value):
    return (OP_PUSH_STR, value)
    
def plus():
    return (OP_PLUS,)
    
def minus():
    return (OP_MINUS,)
    
def multiply():
    return (OP_MULT,)
    
def divide():
    return (OP_DIV,)
    
def modulo():
    return (OP_MOD,)
    
def bitwise_and():
    return (OP_AND,)
    
def bitwise_or():
    return (OP_OR,)
    
def bitwise_xor():
    return (OP_XOR,)
    
def bitwise_not():
    return (OP_NOT,)
    
def equals():
    return (OP_EQ,)
    
def not_equals():
    return (OP_NEQ,)
    
def greater_than():
    return (OP_GT,)
    
def less_than():
    return (OP_LT,)
    
def dump():
    return (OP_DUMP,)
    
def set_var(name):
    return (OP_SET_VAR, name)
    
def get_var(name):
    return (OP_GET_VAR, name)
    
def func_def(name, body):
    return (OP_FUNC_DEF, name, body)
    
def func_call(name):
    return (OP_FUNC_CALL, name)
    
def return_op():
    return (OP_RETURN,)
    
def array_new():
    return (OP_ARRAY_NEW,)
    
def array_set():
    return (OP_ARRAY_SET,)
    
def array_get():
    return (OP_ARRAY_GET,)
    
def array_len():
    return (OP_ARRAY_LEN,)
    
def str_concat():
    return (OP_STR_CONCAT,)
    
def str_length():
    return (OP_STR_LENGTH,)
    
def str_slice():
    return (OP_STR_SLICE,)
    
def str_contains():
    return (OP_STR_CONTAINS,)
    
def str_split():
    return (OP_STR_SPLIT,)
    
def str_convert():
    return (OP_STR,)
    
def file_open():
    return (OP_FILE_OPEN,)
    
def file_close():
    return (OP_FILE_CLOSE,)
    
def file_read():
    return (OP_FILE_READ,)
    
def file_write():
    return (OP_FILE_WRITE,)
    
def file_append():
    return (OP_FILE_APPEND,)

def parse_program(tokens):
    """Parse a list of tokens into a Backstack program"""
    program = []
    i = 0
    
    while i < len(tokens):
        token = tokens[i]
        
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            program.append((OP_PUSH, int(token)))
        elif token[0] == '"' and token[-1] == '"':
            # String literal
            program.append((OP_PUSH_STR, token[1:-1]))
        elif token == "+":
            program.append((OP_PLUS,))
        elif token == "-":
            program.append((OP_MINUS,))
        elif token == "*":
            program.append((OP_MULT,))
        elif token == "/":
            program.append((OP_DIV,))
        elif token == "%":
            program.append((OP_MOD,))
        elif token == "&":
            program.append((OP_AND,))
        elif token == "|":
            program.append((OP_OR,))
        elif token == "^":
            program.append((OP_XOR,))
        elif token == "~":
            program.append((OP_NOT,))
        elif token == "==":
            program.append((OP_EQ,))
        elif token == "!=":
            program.append((OP_NEQ,))
        elif token == ">":
            program.append((OP_GT,))
        elif token == "<":
            program.append((OP_LT,))
        elif token == "dump":
            program.append((OP_DUMP,))
        elif token.startswith("set:"):
            var_name = token[4:]
            program.append((OP_SET_VAR, var_name))
        elif token.startswith("get:"):
            var_name = token[4:]
            program.append((OP_GET_VAR, var_name))
        elif token.startswith("fun:"):
            func_name = token[4:]
            func_body = []
            i += 1
            nesting = 0
            while i < len(tokens) and (tokens[i] != "fun_end" or nesting > 0):
                if tokens[i].startswith("fun:"):
                    nesting += 1
                elif tokens[i] == "fun_end":
                    nesting -= 1
                func_body.append(tokens[i])
                i += 1
            program.append((OP_FUNC_DEF, func_name, parse_program(func_body)))
        elif token.startswith("call:"):
            func_name = token[5:]
            program.append((OP_FUNC_CALL, func_name))
        elif token == "return":
            program.append((OP_RETURN,))
        elif token == "array_new":
            program.append((OP_ARRAY_NEW,))
        elif token == "array_set":
            program.append((OP_ARRAY_SET,))
        elif token == "array_get":
            program.append((OP_ARRAY_GET,))
        elif token == "array_len":
            program.append((OP_ARRAY_LEN,))
        elif token == "str_concat":
            program.append((OP_STR_CONCAT,))
        elif token == "str_length":
            program.append((OP_STR_LENGTH,))
        elif token == "str_slice":
            program.append((OP_STR_SLICE,))
        elif token == "str_contains":
            program.append((OP_STR_CONTAINS,))
        elif token == "str_split":
            program.append((OP_STR_SPLIT,))
        elif token == "str_convert":
            program.append((OP_STR,))
        elif token == "file_open":
            program.append((OP_FILE_OPEN,))
        elif token == "file_close":
            program.append((OP_FILE_CLOSE,))
        elif token == "file_read":
            program.append((OP_FILE_READ,))
        elif token == "file_write":
            program.append((OP_FILE_WRITE,))
        elif token == "file_append":
            program.append((OP_FILE_APPEND,))
            
        i += 1
        
    return program

def tokenize(text):
    """Convert program text to tokens"""
    result = []
    i = 0
    
    while i < len(text):
        # Skip whitespace
        if text[i].isspace():
            i += 1
            continue
            
        # Handle comments
        if text[i] == '#':
            while i < len(text) and text[i] != '\n':
                i += 1
            continue
            
        # Handle string literals
        if text[i] == '"':
            start = i
            i += 1
            while i < len(text) and text[i] != '"':
                if text[i] == '\\' and i + 1 < len(text):
                    i += 2  # Skip escaped character
                else:
                    i += 1
            i += 1  # Skip closing quote
            result.append(text[start:i])
            continue
            
        # Handle other tokens
        if text[i].isalnum() or text[i] in "_:":
            start = i
            while i < len(text) and (text[i].isalnum() or text[i] in "_:"):
                i += 1
            result.append(text[start:i])
        elif text[i] in "+-*/%&|^~<>=!":
            if i + 1 < len(text) and text[i:i+2] in ["==", "!="]:
                result.append(text[i:i+2])
                i += 2
            else:
                result.append(text[i])
                i += 1
        else:
            result.append(text[i])
            i += 1
            
    return result

def read_program_from_file(filename):
    """Read a Backstack program from a file"""
    try:
        with open(filename, "r") as f:
            text = f.read()
        tokens = tokenize(text)
        return parse_program(tokens)
    except Exception as e:
        print(f"ERROR: Could not read program from file: {e}")
        return []

def read_program_from_args(args):
    """Read a Backstack program from command line arguments"""
    tokens = args
    return parse_program(tokens)

def usage():
    """Print usage information"""
    print("Backstack - a stack-based programming language")
    print("Usage:")
    print("  python main.py sim [program arguments]  - Simulate a program")
    print("  python main.py com [source.bs] [output] - Compile a program to assembly")
    print("  python main.py run [source.bs]          - Compile and run a program")
    print("  python main.py help                     - Show this help message")
    
def simulate_program(program):
    """Simulate a Backstack program"""
    stack = []
    variables = {}
    functions = {}
    arrays = {}
    files = {}  # Map file handles to file objects
    
    # Preprocess to extract functions
    for op in program:
        if op[0] == OP_FUNC_DEF:
            func_name, func_body = op[1], op[2]
            functions[func_name] = func_body
            
    i = 0
    call_stack = []
    
    while i < len(program):
        op = program[i]
        
        if op[0] == OP_PUSH:
            stack.append(op[1])
        elif op[0] == OP_PUSH_STR:
            stack.append(op[1])
        elif op[0] == OP_PLUS:
            if len(stack) < 2:
                print("ERROR: Not enough values for PLUS operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif op[0] == OP_MINUS:
            if len(stack) < 2:
                print("ERROR: Not enough values for MINUS operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif op[0] == OP_MULT:
            if len(stack) < 2:
                print("ERROR: Not enough values for MULT operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif op[0] == OP_DIV:
            if len(stack) < 2:
                print("ERROR: Not enough values for DIV operation")
                return
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                print("ERROR: Division by zero")
                return
            stack.append(a // b)
        elif op[0] == OP_MOD:
            if len(stack) < 2:
                print("ERROR: Not enough values for MOD operation")
                return
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                print("ERROR: Modulo by zero")
                return
            stack.append(a % b)
        elif op[0] == OP_AND:
            if len(stack) < 2:
                print("ERROR: Not enough values for AND operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)
        elif op[0] == OP_OR:
            if len(stack) < 2:
                print("ERROR: Not enough values for OR operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)
        elif op[0] == OP_XOR:
            if len(stack) < 2:
                print("ERROR: Not enough values for XOR operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(a ^ b)
        elif op[0] == OP_NOT:
            if not stack:
                print("ERROR: Not enough values for NOT operation")
                return
            a = stack.pop()
            stack.append(~a)
        elif op[0] == OP_EQ:
            if len(stack) < 2:
                print("ERROR: Not enough values for EQ operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a == b else 0)
        elif op[0] == OP_NEQ:
            if len(stack) < 2:
                print("ERROR: Not enough values for NEQ operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a != b else 0)
        elif op[0] == OP_GT:
            if len(stack) < 2:
                print("ERROR: Not enough values for GT operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a > b else 0)
        elif op[0] == OP_LT:
            if len(stack) < 2:
                print("ERROR: Not enough values for LT operation")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(1 if a < b else 0)
        elif op[0] == OP_DUMP:
            if not stack:
                print("ERROR: Not enough values for DUMP operation")
                return
            print(stack.pop())
        elif op[0] == OP_SET_VAR:
            if not stack:
                print("ERROR: Not enough values for SET_VAR operation")
                return
            var_name = op[1]
            variables[var_name] = stack.pop()
        elif op[0] == OP_GET_VAR:
            var_name = op[1]
            if var_name not in variables:
                print(f"ERROR: Variable '{var_name}' not defined")
                return
            stack.append(variables[var_name])
        elif op[0] == OP_FUNC_DEF:
            # Skip function definitions during execution (already preprocessed)
            pass
        elif op[0] == OP_FUNC_CALL:
            func_name = op[1]
            if func_name not in functions:
                print(f"ERROR: Function '{func_name}' not defined")
                return
            # Push current position to call stack
            call_stack.append(i)
            # Set program counter to function body
            program = functions[func_name]
            i = -1  # Will be incremented to 0
        elif op[0] == OP_RETURN:
            if not call_stack:
                print("ERROR: RETURN outside of function")
                return
            # Return to caller
            i = call_stack.pop()
            program = program  # Return to original program
        elif op[0] == OP_ARRAY_NEW:
            if not stack:
                print("ERROR: Need size to create array")
                return
            size = stack.pop()
            if not isinstance(size, int) or size < 0:
                print("ERROR: Array size must be a non-negative integer")
                return
            array_id = len(arrays)
            arrays[array_id] = [0] * size
            stack.append(array_id)
        elif op[0] == OP_ARRAY_SET:
            if len(stack) < 3:
                print("ERROR: Need array, index, value for ARRAY_SET")
                return
            value = stack.pop()
            index = stack.pop()
            array_id = stack.pop()
            
            if array_id not in arrays:
                print(f"ERROR: Invalid array ID: {array_id}")
                return
                
            array = arrays[array_id]
            if not isinstance(index, int) or index < 0 or index >= len(array):
                print(f"ERROR: Array index out of bounds: {index}")
                return
                
            array[index] = value
        elif op[0] == OP_ARRAY_GET:
            if len(stack) < 2:
                print("ERROR: Need array and index for ARRAY_GET")
                return
            index = stack.pop()
            array_id = stack.pop()
            
            if array_id not in arrays:
                print(f"ERROR: Invalid array ID: {array_id}")
                return
                
            array = arrays[array_id]
            if not isinstance(index, int) or index < 0 or index >= len(array):
                print(f"ERROR: Array index out of bounds: {index}")
                return
                
            stack.append(array[index])
        elif op[0] == OP_ARRAY_LEN:
            if not stack:
                print("ERROR: Need array for ARRAY_LEN")
                return
            array_id = stack.pop()
            
            if array_id not in arrays:
                print(f"ERROR: Invalid array ID: {array_id}")
                return
                
            stack.append(len(arrays[array_id]))
        elif op[0] == OP_STR_CONCAT:
            if len(stack) < 2:
                print("ERROR: Need two strings for STR_CONCAT")
                return
            b = stack.pop()
            a = stack.pop()
            stack.append(str(a) + str(b))
        elif op[0] == OP_STR_LENGTH:
            if not stack:
                print("ERROR: Need string for STR_LENGTH")
                return
            s = stack.pop()
            stack.append(len(str(s)))
        elif op[0] == OP_STR_SLICE:
            if len(stack) < 3:
                print("ERROR: Need string, start, end for STR_SLICE")
                return
            end = stack.pop()
            start = stack.pop()
            s = stack.pop()
            
            try:
                stack.append(str(s)[start:end])
            except IndexError:
                print(f"ERROR: String slice indices out of range: {start}:{end}")
                return
        elif op[0] == OP_STR_CONTAINS:
            if len(stack) < 2:
                print("ERROR: Need string and substring for STR_CONTAINS")
                return
            substring = stack.pop()
            s = stack.pop()
            stack.append(1 if str(substring) in str(s) else 0)
        elif op[0] == OP_STR_SPLIT:
            if len(stack) < 2:
                print("ERROR: Need string and delimiter for STR_SPLIT")
                return
            delimiter = stack.pop()
            s = stack.pop()
            
            # Create a new array for the split parts
            parts = str(s).split(str(delimiter))
            array_id = len(arrays)
            arrays[array_id] = parts
            stack.append(array_id)
        elif op[0] == OP_STR:
            if not stack:
                print("ERROR: Need value for STR conversion")
                return
            value = stack.pop()
            stack.append(str(value))
        elif op[0] == OP_FILE_OPEN:
            if len(stack) < 2:
                print("ERROR: Need filename and mode for FILE_OPEN")
                return
            mode = stack.pop()
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
                files[file_handle].flush()
            except Exception as e:
                print(f"ERROR: Could not append to file: {e}")
                return
        
        i += 1
    
    # Close any open files
    for handle in files:
        try:
            files[handle].close()
        except:
            pass

def call_cmd(cmd, args=None):
    if args is None:
        args = []
    command_line = [cmd] + args
    try:
        import subprocess
        result = subprocess.run(command_line, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode
    except Exception as e:
        print(f"Error executing command: {e}")
        return -1
