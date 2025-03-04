
import os
from . import backstack

class AsmGenerator:
    def __init__(self):
        self.output = []
        self.label_counter = 0
        self.string_literals = []
        self.variables = {}
        
    def generate_unique_label(self, prefix="label"):
        """Generate a unique label for jumps and conditionals"""
        label = f"{prefix}_{self.label_counter}"
        self.label_counter += 1
        return label
        
    def add_string_literal(self, string):
        """Add a string literal to the data section and return its label"""
        label = f"str_{len(self.string_literals)}"
        self.string_literals.append((label, string))
        return label
        
    def emit(self, line):
        """Add a line of assembly code"""
        self.output.append(line)
        
    def emit_header(self):
        """Generate the assembly header"""
        self.emit("; Backstack compiled program")
        self.emit("bits 64")
        self.emit("default rel")
        self.emit("")
        self.emit("; External functions")
        self.emit("extern ExitProcess")
        self.emit("extern printf")
        self.emit("extern GetStdHandle")
        self.emit("extern WriteConsoleA")
        self.emit("extern malloc")
        self.emit("extern free")
        self.emit("extern strlen")
        self.emit("extern strcpy")
        self.emit("extern strcat")
        self.emit("extern strstr")
        self.emit("extern strdup")
        self.emit("extern sprintf")
        self.emit("extern fopen")
        self.emit("extern fclose")
        self.emit("extern fseek")
        self.emit("extern ftell")
        self.emit("extern fread")
        self.emit("extern fputs")
        self.emit("")
        self.emit("section .data")
        self.emit('    fmt_int db "%lld", 10, 0')
        self.emit('    fmt_bool_true db "true", 10, 0')
        self.emit('    fmt_bool_false db "false", 10, 0')
        self.emit('    fmt_str db "%s", 10, 0')
        self.emit('    array_error_msg db "Array index out of bounds", 10, 0')
        self.emit('    file_error_msg db "File operation error", 10, 0')
        self.emit("")
        
    def emit_string_literals(self):
        """Emit all string literals to the data section"""
        for label, string in self.string_literals:
            escaped_str = string.replace('"', '\\"')
            self.emit(f'    {label} db "{escaped_str}", 0')
        self.emit("")
        
    def emit_footer(self):
        """Generate the assembly footer"""
        self.emit("section .text")
        self.emit("    global main")
        self.emit("")
        
        # Print functions
        self.emit_print_functions()
        
        # Main function
        self.emit("main:")
        self.emit("    ; Function prologue")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")  # Reserve shadow space for Windows calling convention
        self.emit("")
        
    def emit_print_functions(self):
        """Emit helper functions for printing values"""
        # Print integer
        self.emit("print_int:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")
        self.emit("    mov rdx, rdi")
        self.emit("    lea rcx, [fmt_int]")
        self.emit("    call printf")
        self.emit("    add rsp, 32")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # Print boolean
        self.emit("print_bool:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")
        self.emit("    test rdi, rdi")
        self.emit("    jz .false")
        self.emit("    lea rcx, [fmt_bool_true]")
        self.emit("    jmp .print")
        self.emit(".false:")
        self.emit("    lea rcx, [fmt_bool_false]")
        self.emit(".print:")
        self.emit("    call printf")
        self.emit("    add rsp, 32")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # Print string
        self.emit("print_string:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")
        self.emit("    mov rdx, rdi")
        self.emit("    lea rcx, [fmt_str]")
        self.emit("    call printf")
        self.emit("    add rsp, 32")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # String concatenation function
        self.emit("strcat_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    push rsi")  # Save original strings
        self.emit("    push rdi")
        self.emit("    call strlen")  # Get length of first string
        self.emit("    mov rbx, rax")  # Store in rbx
        self.emit("    mov rdi, [rbp-16]")  # Load second string
        self.emit("    call strlen")  # Get length of second string
        self.emit("    add rax, rbx")  # Add lengths
        self.emit("    add rax, 1")  # Add 1 for null terminator
        self.emit("    mov rdi, rax")  # Set as parameter for malloc
        self.emit("    call malloc")  # Allocate memory
        self.emit("    mov rdi, rax")  # Set as destination for strcpy
        self.emit("    mov rsi, [rbp-8]")  # Load first string as source
        self.emit("    call strcpy")  # Copy first string
        self.emit("    mov rdi, rax")  # Set result as destination
        self.emit("    mov rsi, [rbp-16]")  # Load second string as source
        self.emit("    call strcat")  # Concatenate second string
        self.emit("    pop rdi")  # Restore saved registers
        self.emit("    pop rsi")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # Substring function
        self.emit("substr_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rdx, rcx")  # Calculate length (end - start)
        self.emit("    add rdx, 1")  # Add 1 for null terminator
        self.emit("    push rsi")  # Save original string
        self.emit("    push rcx")  # Save start index
        self.emit("    push rdx")  # Save length
        self.emit("    mov rdi, rdx")  # Set size for malloc
        self.emit("    call malloc")  # Allocate memory
        self.emit("    pop rdx")  # Restore length
        self.emit("    pop rcx")  # Restore start index
        self.emit("    pop rsi")  # Restore original string
        self.emit("    add rsi, rcx")  # Add start offset to source
        self.emit("    mov rdi, rax")  # Set destination
        self.emit("    mov rcx, rdx")  # Set count
        self.emit("    rep movsb")  # Copy bytes
        self.emit("    mov byte [rdi], 0")  # Null-terminate
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # String split function
        self.emit("str_split_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Placeholder for string split implementation")
        self.emit("    ; In a real implementation, this would tokenize the string")
        self.emit("    mov rax, 0")  # Return empty array for now
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # Integer to string conversion
        self.emit("int_to_str_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")
        self.emit("    lea rsi, [fmt_int]")  # Format string
        self.emit("    mov rdx, rdi")  # Integer value
        self.emit("    mov rdi, rsp")  # Buffer on stack
        self.emit("    xor rax, rax")
        self.emit("    call sprintf")  # Call sprintf
        self.emit("    mov rdi, rsp")  # Set buffer as parameter
        self.emit("    call strdup")  # Duplicate the string
        self.emit("    add rsp, 32")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # File read function
        self.emit("file_read_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Implementation would read file contents")
        self.emit("    ; Using fseek, ftell, malloc, and fread")
        self.emit("    mov rax, 0")  # Return empty string for now
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # File write function
        self.emit("file_write_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Implementation would write to file using fputs")
        self.emit("    mov rax, 0")  # Return success
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # File append function
        self.emit("file_append_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Implementation would append to file")
        self.emit("    mov rax, 0")  # Return success
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")
        
        # Array index error handler
        self.emit("array_index_error:")
        self.emit("    ; Handle array index out of bounds")
        self.emit("    lea rcx, [array_error_msg]")
        self.emit("    call printf")
        self.emit("    xor rcx, rcx")
        self.emit("    call ExitProcess")
        self.emit("")
        
    def emit_main_end(self):
        """Emit the end of the main function"""
        self.emit("    ; Exit program")
        self.emit("    xor rcx, rcx")
        self.emit("    call ExitProcess")
        
    def compile_push(self, value):
        """Compile a PUSH operation"""
        self.emit(f"    ; Push {value}")
        self.emit(f"    mov rax, {value}")
        self.emit("    push rax")
        
    def compile_push_string(self, string):
        """Compile a string literal push operation"""
        string_label = self.add_string_literal(string)
        self.emit(f"    ; Push string \"{string}\"")
        self.emit(f"    lea rax, [{string_label}]")
        self.emit("    push rax")
        
    def compile_plus(self):
        """Compile a PLUS operation"""
        self.emit("    ; Add top two values")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    add rax, rbx")
        self.emit("    push rax")
        
    def compile_minus(self):
        """Compile a MINUS operation"""
        self.emit("    ; Subtract top from second")
        self.emit("    pop rbx")  # second operand
        self.emit("    pop rax")  # first operand
        self.emit("    sub rax, rbx")
        self.emit("    push rax")
        
    def compile_multiply(self):
        """Compile a MULTIPLY operation"""
        self.emit("    ; Multiply top two values")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    imul rax, rbx")
        self.emit("    push rax")
        
    def compile_divide(self):
        """Compile a DIVIDE operation"""
        self.emit("    ; Divide second by top")
        self.emit("    pop rbx")  # divisor
        self.emit("    pop rax")  # dividend
        self.emit("    cqo")      # sign-extend RAX into RDX:RAX
        self.emit("    idiv rbx")
        self.emit("    push rax")
        
    def compile_modulo(self):
        """Compile a MODULO operation"""
        self.emit("    ; Modulo second by top")
        self.emit("    pop rbx")  # divisor
        self.emit("    pop rax")  # dividend
        self.emit("    cqo")      # sign-extend RAX into RDX:RAX
        self.emit("    idiv rbx")
        self.emit("    push rdx") # remainder is in RDX
        
    def compile_bitwise_and(self):
        """Compile a BITWISE AND operation"""
        self.emit("    ; Bitwise AND")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    and rax, rbx")
        self.emit("    push rax")
        
    def compile_bitwise_or(self):
        """Compile a BITWISE OR operation"""
        self.emit("    ; Bitwise OR")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    or rax, rbx")
        self.emit("    push rax")
        
    def compile_bitwise_xor(self):
        """Compile a BITWISE XOR operation"""
        self.emit("    ; Bitwise XOR")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    xor rax, rbx")
        self.emit("    push rax")
        
    def compile_bitwise_not(self):
        """Compile a BITWISE NOT operation"""
        self.emit("    ; Bitwise NOT")
        self.emit("    pop rax")
        self.emit("    not rax")
        self.emit("    push rax")
        
    def compile_equals(self):
        """Compile an EQUALS operation"""
        self.emit("    ; Equals comparison")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    cmp rax, rbx")
        self.emit("    sete al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")
        
    def compile_not_equals(self):
        """Compile a NOT EQUALS operation"""
        self.emit("    ; Not equals comparison")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    cmp rax, rbx")
        self.emit("    setne al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")
        
    def compile_greater_than(self):
        """Compile a GREATER THAN operation"""
        self.emit("    ; Greater than comparison")
        self.emit("    pop rbx")  # second operand
        self.emit("    pop rax")  # first operand
        self.emit("    cmp rax, rbx")
        self.emit("    setg al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")
        
    def compile_less_than(self):
        """Compile a LESS THAN operation"""
        self.emit("    ; Less than comparison")
        self.emit("    pop rbx")  # second operand
        self.emit("    pop rax")  # first operand
        self.emit("    cmp rax, rbx")
        self.emit("    setl al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")
        
    def compile_dump(self):
        """Compile a DUMP operation"""
        self.emit("    ; Dump (print) top value")
        self.emit("    pop rdi")
        self.emit("    call print_int")
        
    def compile_if_start(self):
        """Compile the start of an IF statement"""
        label = self.generate_unique_label("if_end")
        self.emit("    ; IF statement")
        self.emit("    pop rax")
        self.emit("    test rax, rax")
        self.emit(f"    jz {label}")
        return label
        
    def compile_if_else(self, end_label):
        """Compile the ELSE part of an IF statement"""
        else_label = self.generate_unique_label("else")
        self.emit(f"    jmp {else_label}")
        self.emit(f"{end_label}:")
        return else_label
        
    def compile_if_end(self, label):
        """Compile the end of an IF statement"""
        self.emit(f"{label}:")
        
    def compile_while_start(self):
        """Compile the start of a WHILE loop"""
        loop_start = self.generate_unique_label("while_start")
        loop_end = self.generate_unique_label("while_end")
        self.emit("    ; WHILE loop")
        self.emit(f"{loop_start}:")
        return (loop_start, loop_end)
        
    def compile_while_condition(self, labels):
        """Compile the condition check of a WHILE loop"""
        loop_start, loop_end = labels
        self.emit("    ; WHILE condition")
        self.emit("    pop rax")
        self.emit("    test rax, rax")
        self.emit(f"    jz {loop_end}")
        
    def compile_while_end(self, labels):
        """Compile the end of a WHILE loop"""
        loop_start, loop_end = labels
        self.emit(f"    jmp {loop_start}")
        self.emit(f"{loop_end}:")
        
    def compile_set_var(self, var_name):
        """Compile a SET_VAR operation"""
        if var_name not in self.variables:
            var_label = f"var_{len(self.variables)}"
            self.variables[var_name] = var_label
            # Add variable to data section
            self.emit(f"    {var_label} dq 0")
        
        var_label = self.variables[var_name]
        self.emit(f"    ; Set variable {var_name}")
        self.emit("    pop rax")
        self.emit(f"    mov [{var_label}], rax")
        
    def compile_get_var(self, var_name):
        """Compile a GET_VAR operation"""
        if var_name not in self.variables:
            raise KeyError(f"Variable '{var_name}' not defined")
            
        var_label = self.variables[var_name]
        self.emit(f"    ; Get variable {var_name}")
        self.emit(f"    mov rax, [{var_label}]")
        self.emit("    push rax")
    
    # Array operations
    def compile_array_new(self):
        """Compile an ARRAY_NEW operation"""
        self.emit("    ; Create a new array")
        self.emit("    pop rax")  # Size of array
        self.emit("    imul rax, 8")  # Calculate bytes needed (8 bytes per element)
        self.emit("    add rax, 8")  # Add 8 bytes for length
        self.emit("    sub rsp, 8")  # Align stack
        self.emit("    mov rcx, rax")  # Size parameter
        self.emit("    call malloc")  # Call malloc
        self.emit("    add rsp, 8")  # Restore stack
        self.emit("    pop rbx")  # Original array size
        self.emit("    mov [rax], rbx")  # Store size at the beginning
        self.emit("    push rax")  # Push array pointer
        
    def compile_array_set(self):
        """Compile an ARRAY_SET operation"""
        self.emit("    ; Set array element")
        self.emit("    pop rcx")  # Value to set
        self.emit("    pop rbx")  # Index
        self.emit("    pop rax")  # Array pointer
        self.emit("    cmp rbx, [rax]")  # Compare index with array length
        self.emit("    jge array_index_error")  # Jump if out of bounds
        self.emit("    lea rax, [rax+8]")  # Skip the length field
        self.emit("    mov [rax+rbx*8], rcx")  # Store value at index
        
    def compile_array_get(self):
        """Compile an ARRAY_GET operation"""
        self.emit("    ; Get array element")
        self.emit("    pop rbx")  # Index
        self.emit("    pop rax")  # Array pointer
        self.emit("    cmp rbx, [rax]")  # Compare index with array length
        self.emit("    jge array_index_error")  # Jump if out of bounds
        self.emit("    lea rax, [rax+8]")  # Skip the length field
        self.emit("    mov rax, [rax+rbx*8]")  # Load value from index
        self.emit("    push rax")  # Push value to stack
        
    def compile_array_len(self):
        """Compile an ARRAY_LEN operation"""
        self.emit("    ; Get array length")
        self.emit("    pop rax")  # Array pointer
        self.emit("    mov rax, [rax]")  # Load length
        self.emit("    push rax")  # Push length to stack
        
    # String operations
    def compile_str_concat(self):
        """Compile a string concatenation operation"""
        self.emit("    ; Concatenate strings")
        self.emit("    pop rdi")  # Second string
        self.emit("    pop rsi")  # First string
        self.emit("    call strcat_func")  # Call helper function
        self.emit("    push rax")  # Push result
        
    def compile_str_length(self):
        """Compile a string length operation"""
        self.emit("    ; Get string length")
        self.emit("    pop rdi")  # String
        self.emit("    call strlen")  # Call C library function
        self.emit("    push rax")  # Push length
        
    def compile_str_slice(self):
        """Compile a string slice operation"""
        self.emit("    ; Slice string")
        self.emit("    pop rdx")  # End index
        self.emit("    pop rcx")  # Start index
        self.emit("    pop rsi")  # String
        self.emit("    call substr_func")  # Call helper function
        self.emit("    push rax")  # Push result
        
    def compile_str_contains(self):
        """Compile a string contains operation"""
        self.emit("    ; Check if string contains substring")
        self.emit("    pop rdi")  # Substring
        self.emit("    pop rsi")  # String
        self.emit("    call strstr")  # Call C library function
        self.emit("    test rax, rax")  # Test if result is NULL
        self.emit("    setnz al")  # Set al to 1 if not NULL (found), 0 otherwise
        self.emit("    movzx rax, al")  # Zero-extend al to rax
        self.emit("    push rax")  # Push result (1 for true, 0 for false)
        
    def compile_str_split(self):
        """Compile a string split operation"""
        self.emit("    ; Split string by delimiter")
        self.emit("    pop rdi")  # Delimiter
        self.emit("    pop rsi")  # String
        self.emit("    call str_split_func")  # Call helper function
        self.emit("    push rax")  # Push array result
        
    def compile_str_convert(self):
        """Compile a value to string conversion"""
        self.emit("    ; Convert value to string")
        self.emit("    pop rdi")  # Value
        self.emit("    call int_to_str_func")  # Call helper function
        self.emit("    push rax")  # Push string result
    
    # File I/O operations
    def compile_file_open(self):
        """Compile a file open operation"""
        self.emit("    ; Open file")
        self.emit("    pop rsi")  # Mode
        self.emit("    pop rdi")  # Filename
        self.emit("    call fopen")  # Call C library function
        self.emit("    push rax")  # Push file handle
        
    def compile_file_close(self):
        """Compile a file close operation"""
        self.emit("    ; Close file")
        self.emit("    pop rdi")  # File handle
        self.emit("    call fclose")  # Call C library function
        self.emit("    push rax")  # Push result
        
    def compile_file_read(self):
        """Compile a file read operation"""
        self.emit("    ; Read file contents")
        self.emit("    pop rdi")  # File handle
        self.emit("    call file_read_func")  # Call helper function
        self.emit("    push rax")  # Push content string
        
    def compile_file_write(self):
        """Compile a file write operation"""
        self.emit("    ; Write to file")
        self.emit("    pop rsi")  # Content
        self.emit("    pop rdi")  # File handle
        self.emit("    call file_write_func")  # Call helper function
        self.emit("    push rax")  # Push result
        
    def compile_file_append(self):
        """Compile a file append operation"""
        self.emit("    ; Append to file")
        self.emit("    pop rsi")  # Content
        self.emit("    pop rdi")  # File handle
        self.emit("    call file_append_func")  # Call helper function
        self.emit("    push rax")  # Push result
        
    def compile_function_def(self, name, body):
        """Compile a function definition"""
        function_label = f"func_{name}"
        self.emit(f"    ; Function definition: {name}")
        self.emit(f"    jmp {function_label}_end  ; Skip over function body")
        self.emit(f"{function_label}:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        
        # Compile the function body
        for op in body:
            self.compile_op(op)
            
        # Handle return - in case there's no explicit return
        self.emit("    pop rax  ; Return value")
        self.emit("    mov rsp, rbp")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit(f"{function_label}_end:")
        
    def compile_function_call(self, name):
        """Compile a function call"""
        function_label = f"func_{name}"
        self.emit(f"    ; Call function: {name}")
        self.emit(f"    call {function_label}")
        self.emit("    push rax  ; Push return value onto stack")
        
    def compile_return(self):
        """Compile a return statement"""
        self.emit("    ; Return from function")
        self.emit("    pop rax  ; Return value")
        self.emit("    mov rsp, rbp")
        self.emit("    pop rbp")
        self.emit("    ret")
        
    def compile_op(self, op):
        """Compile a single operation"""
        if op[0] == backstack.OP_PUSH:
            self.compile_push(op[1])
        elif op[0] == backstack.OP_PUSH_STR:
            self.compile_push_string(op[1])
        elif op[0] == backstack.OP_PLUS:
            self.compile_plus()
        elif op[0] == backstack.OP_MINUS:
            self.compile_minus()
        elif op[0] == backstack.OP_MULT:
            self.compile_multiply()
        elif op[0] == backstack.OP_DIV:
            self.compile_divide()
        elif op[0] == backstack.OP_MOD:
            self.compile_modulo()
        elif op[0] == backstack.OP_AND:
            self.compile_bitwise_and()
        elif op[0] == backstack.OP_OR:
            self.compile_bitwise_or()
        elif op[0] == backstack.OP_XOR:
            self.compile_bitwise_xor()
        elif op[0] == backstack.OP_NOT:
            self.compile_bitwise_not()
        elif op[0] == backstack.OP_EQ:
            self.compile_equals()
        elif op[0] == backstack.OP_NEQ:
            self.compile_not_equals()
        elif op[0] == backstack.OP_GT:
            self.compile_greater_than()
        elif op[0] == backstack.OP_LT:
            self.compile_less_than()
        elif op[0] == backstack.OP_DUMP:
            self.compile_dump()
        elif op[0] == backstack.OP_SET_VAR:
            self.compile_set_var(op[1])
        elif op[0] == backstack.OP_GET_VAR:
            self.compile_get_var(op[1])
        elif op[0] == backstack.OP_FUNC_DEF:
            self.compile_function_def(op[1], op[2])
        elif op[0] == backstack.OP_FUNC_CALL:
            self.compile_function_call(op[1])
        elif op[0] == backstack.OP_RETURN:
            self.compile_return()
        # Array operations
        elif op[0] == backstack.OP_ARRAY_NEW:
            self.compile_array_new()
        elif op[0] == backstack.OP_ARRAY_SET:
            self.compile_array_set()
        elif op[0] == backstack.OP_ARRAY_GET:
            self.compile_array_get()
        elif op[0] == backstack.OP_ARRAY_LEN:
            self.compile_array_len()
        # String operations
        elif op[0] == backstack.OP_STR_CONCAT:
            self.compile_str_concat()
        elif op[0] == backstack.OP_STR_LENGTH:
            self.compile_str_length()
        elif op[0] == backstack.OP_STR_SLICE:
            self.compile_str_slice()
        elif op[0] == backstack.OP_STR_CONTAINS:
            self.compile_str_contains()
        elif op[0] == backstack.OP_STR_SPLIT:
            self.compile_str_split()
        elif op[0] == backstack.OP_STR:
            self.compile_str_convert()
        # File I/O operations
        elif op[0] == backstack.OP_FILE_OPEN:
            self.compile_file_open()
        elif op[0] == backstack.OP_FILE_CLOSE:
            self.compile_file_close()
        elif op[0] == backstack.OP_FILE_READ:
            self.compile_file_read()
        elif op[0] == backstack.OP_FILE_WRITE:
            self.compile_file_write()
        elif op[0] == backstack.OP_FILE_APPEND:
            self.compile_file_append()
        else:
            raise ValueError(f"Unsupported operation for compilation: {op}")
    
    def compile_program(self, program):
        """Compile a Backstack program to assembly code"""
        # Initialize output
        self.output = []
        self.variables = {}
        
        # Generate header
        self.emit_header()
        
        # Add variables section
        self.emit("    ; Variables")
        
        # Process program to collect string literals and variables
        for op in program:
            if op[0] == backstack.OP_PUSH_STR:
                self.add_string_literal(op[1])
                
        # Emit string literals
        self.emit_string_literals()
        
        # Generate footer with main function
        self.emit_footer()
        
        # Compile program operations
        for op in program:
            self.compile_op(op)
            
        # End main function
        self.emit_main_end()
        
        # Return the complete assembly code
        return "\n".join(self.output)
