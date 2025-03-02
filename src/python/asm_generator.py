
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
        self.emit("")
        self.emit("section .data")
        self.emit('    fmt_int db "%lld", 10, 0')
        self.emit('    fmt_bool_true db "true", 10, 0')
        self.emit('    fmt_bool_false db "false", 10, 0')
        self.emit('    fmt_str db "%s", 10, 0')
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
