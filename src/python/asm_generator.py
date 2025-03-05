import os
from src.python.backstack import OP_PUSH, OP_PUSH_STR, OP_PLUS, OP_MINUS, OP_MULTI, OP_DIVIDE
from src.python.backstack import OP_MOD, OP_DUMP, OP_SET, OP_GET, OP_IF, OP_ELSE, OP_ENDIF
from src.python.backstack import OP_GREATER, OP_LESS, OP_EQUAL, OP_NOT_EQUAL, OP_LESS_EQUAL
from src.python.backstack import OP_BIT_AND, OP_BIT_OR, OP_BIT_XOR, OP_BIT_NOT
from src.python.backstack import OP_DUP, OP_SWAP, OP_DROP, OP_OVER, OP_ROT
from src.python.backstack import OP_WHILE, OP_REPEAT, OP_FOR, OP_NEXT
from src.python.backstack import OP_FUN_DEF, OP_FUN_END, OP_FUN_CALL, OP_RETURN
from src.python.backstack import OP_ARRAY_NEW, OP_ARRAY_SET, OP_ARRAY_GET, OP_ARRAY_LEN
from src.python.backstack import OP_STR_CONCAT, OP_STR_LENGTH, OP_STR_SLICE, OP_STR_CONTAINS, OP_STR_SPLIT, OP_STR
from src.python.backstack import OP_FILE_OPEN, OP_FILE_CLOSE, OP_FILE_READ, OP_FILE_WRITE, OP_FILE_APPEND

class AsmGenerator:
    def __init__(self):
        self.output = []
        self.label_counter = 0
        self.string_literals = []
        self.variables = {}
        self.if_stack = []
        self.loop_stack = []
        self.func_labels = {}
        self.platform = self._detect_platform()

    def _detect_platform(self):
        """Detect the current platform"""
        if os.name == 'nt':
            return 'windows'
        elif os.name == 'posix':
            return 'linux'  # This includes macOS as well
        else:
            return 'unknown'

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

    def emit_data_section(self):
        """Generate the data section"""
        self.emit("section .data")
        self.emit("    fmt_int db \"%lld\", 10, 0")
        self.emit("    fmt_bool_true db \"true\", 10, 0")
        self.emit("    fmt_bool_false db \"false\", 10, 0")
        self.emit("    fmt_str db \"%s\", 10, 0")
        self.emit("    array_error_msg db \"Array index out of bounds\", 10, 0")
        self.emit("    file_error_msg db \"File operation error\", 10, 0")
        self.emit("")

        # Output string literals
        self.emit("    ; Variables")
        for label, string in self.string_literals:
            # Escape any special characters in the string
            escaped_string = string.replace('\\', '\\\\').replace('"', '\\"')
            self.emit(f"    {label} db \"{escaped_string}\", 0")
        self.emit("")

    def emit_helper_functions(self):
        """Generate helper functions for the runtime"""
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

        # String functions
        self.emit("strcat_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    push rsi")
        self.emit("    push rdi")
        self.emit("    call strlen")
        self.emit("    mov rbx, rax")
        self.emit("    mov rdi, [rbp-16]")
        self.emit("    call strlen")
        self.emit("    add rax, rbx")
        self.emit("    add rax, 1")
        self.emit("    mov rdi, rax")
        self.emit("    call malloc")
        self.emit("    mov rdi, rax")
        self.emit("    mov rsi, [rbp-8]")
        self.emit("    call strcpy")
        self.emit("    mov rdi, rax")
        self.emit("    mov rsi, [rbp-16]")
        self.emit("    call strcat")
        self.emit("    pop rdi")
        self.emit("    pop rsi")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        # String substr function
        self.emit("substr_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rdx, rcx")
        self.emit("    add rdx, 1")
        self.emit("    push rsi")
        self.emit("    push rcx")
        self.emit("    push rdx")
        self.emit("    mov rdi, rdx")
        self.emit("    call malloc")
        self.emit("    pop rdx")
        self.emit("    pop rcx")
        self.emit("    pop rsi")
        self.emit("    add rsi, rcx")
        self.emit("    mov rdi, rax")
        self.emit("    mov rcx, rdx")
        self.emit("    rep movsb")
        self.emit("    mov byte [rdi], 0")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        # String split function (placeholder)
        self.emit("str_split_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Placeholder for string split implementation")
        self.emit("    ; In a real implementation, this would tokenize the string")
        self.emit("    mov rax, 0")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        # Integer to string function
        self.emit("int_to_str_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")
        self.emit("    lea rsi, [fmt_int]")
        self.emit("    mov rdx, rdi")
        self.emit("    mov rdi, rsp")
        self.emit("    xor rax, rax")
        self.emit("    call sprintf")
        self.emit("    mov rdi, rsp")
        self.emit("    call strdup")
        self.emit("    add rsp, 32")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        # File operation functions
        self.emit("file_read_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Implementation would read file contents")
        self.emit("    ; Using fseek, ftell, malloc, and fread")
        self.emit("    mov rax, 0")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        self.emit("file_write_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Implementation would write to file using fputs")
        self.emit("    mov rax, 0")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        self.emit("file_append_func:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    ; Implementation would append to file")
        self.emit("    mov rax, 0")
        self.emit("    pop rbp")
        self.emit("    ret")
        self.emit("")

        # Array bounds error handler
        self.emit("array_index_error:")
        self.emit("    ; Handle array index out of bounds")
        self.emit("    lea rcx, [array_error_msg]")
        self.emit("    call printf")
        self.emit("    xor rcx, rcx")
        self.emit("    call ExitProcess")
        self.emit("")

        # File operation error handler
        self.emit("file_error:")
        self.emit("    ; Handle file operation error")
        self.emit("    lea rcx, [file_error_msg]")
        self.emit("    call printf")
        self.emit("    xor rcx, rcx")
        self.emit("    call ExitProcess")
        self.emit("")

    def emit_text_section(self):
        """Generate the text section"""
        self.emit("section .text")
        self.emit("    global main")
        self.emit("")

    def emit_main_prologue(self):
        """Generate the main function prologue"""
        self.emit("main:")
        self.emit("    ; Function prologue")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        self.emit("    sub rsp, 32")
        self.emit("")

    def emit_main_epilogue(self):
        """Generate the main function epilogue"""
        self.emit("    ; Exit program")
        self.emit("    xor rcx, rcx")
        self.emit("    call ExitProcess")
        self.emit("")

    def compile_program(self, program):
        """
        Compile a Backstack program to assembly

        Args:
            program (list): List of Backstack operations

        Returns:
            str: Generated assembly code
        """
        # Reset state
        self.output = []
        self.label_counter = 0
        self.string_literals = []
        self.variables = {}
        self.if_stack = []
        self.loop_stack = []
        self.func_labels = {}

        # First pass: collect string literals and functions
        for i, op in enumerate(program):
            if op[0] == OP_PUSH_STR:
                self.add_string_literal(op[1])
            elif op[0] == OP_FUN_DEF:
                func_name = op[1]
                label = f"func_{func_name}"
                self.func_labels[func_name] = label

        # Generate assembly
        self.emit_header()
        self.emit_data_section()
        self.emit_text_section()
        self.emit_helper_functions()
        self.emit_main_prologue()

        # Second pass: generate code
        for op in program:
            self.compile_op(op)

        self.emit_main_epilogue()

        return "\n".join(self.output)

    def compile_op(self, op):
        """Compile a single Backstack operation to assembly"""
        op_type = op[0]

        if op_type == OP_PUSH:
            self.compile_push(op[1])
        elif op_type == OP_PUSH_STR:
            self.compile_push_str(op[1])
        elif op_type == OP_PLUS:
            self.compile_plus()
        elif op_type == OP_MINUS:
            self.compile_minus()
        elif op_type == OP_MULTI:
            self.compile_multi()
        elif op_type == OP_DIVIDE:
            self.compile_divide()
        elif op_type == OP_MOD:
            self.compile_mod()
        elif op_type == OP_DUMP:
            self.compile_dump()
        elif op_type == OP_SET:
            self.compile_set(op[1])
        elif op_type == OP_GET:
            self.compile_get(op[1])
        elif op_type == OP_IF:
            self.compile_if()
        elif op_type == OP_ELSE:
            self.compile_else()
        elif op_type == OP_ENDIF:
            self.compile_endif()
        elif op_type == OP_GREATER:
            self.compile_greater()
        elif op_type == OP_LESS:
            self.compile_less()
        elif op_type == OP_EQUAL:
            self.compile_equal()
        elif op_type == OP_NOT_EQUAL:
            self.compile_not_equal()
        elif op_type == OP_LESS_EQUAL:
            self.compile_less_equal()
        elif op_type == OP_BIT_AND:
            self.compile_bit_and()
        elif op_type == OP_BIT_OR:
            self.compile_bit_or()
        elif op_type == OP_BIT_XOR:
            self.compile_bit_xor()
        elif op_type == OP_BIT_NOT:
            self.compile_bit_not()
        elif op_type == OP_DUP:
            self.compile_dup()
        elif op_type == OP_SWAP:
            self.compile_swap()
        elif op_type == OP_DROP:
            self.compile_drop()
        elif op_type == OP_OVER:
            self.compile_over()
        elif op_type == OP_ROT:
            self.compile_rot()
        elif op_type == OP_WHILE:
            self.compile_while()
        elif op_type == OP_REPEAT:
            self.compile_repeat()
        elif op_type == OP_FOR:
            self.compile_for()
        elif op_type == OP_NEXT:
            self.compile_next()
        elif op_type == OP_FUN_DEF:
            self.compile_fun_def(op[1])
        elif op_type == OP_FUN_END:
            self.compile_fun_end()
        elif op_type == OP_FUN_CALL:
            self.compile_fun_call(op[1])
        elif op_type == OP_RETURN:
            self.compile_return()
        elif op_type == OP_ARRAY_NEW:
            self.compile_array_new()
        elif op_type == OP_ARRAY_SET:
            self.compile_array_set()
        elif op_type == OP_ARRAY_GET:
            self.compile_array_get()
        elif op_type == OP_ARRAY_LEN:
            self.compile_array_len()
        elif op_type == OP_STR_CONCAT:
            self.compile_str_concat()
        elif op_type == OP_STR_LENGTH:
            self.compile_str_length()
        elif op_type == OP_STR_SLICE:
            self.compile_str_slice()
        elif op_type == OP_STR_CONTAINS:
            self.compile_str_contains()
        elif op_type == OP_STR_SPLIT:
            self.compile_str_split()
        elif op_type == OP_STR:
            self.compile_str()
        elif op_type == OP_FILE_OPEN:
            self.compile_file_open()
        elif op_type == OP_FILE_CLOSE:
            self.compile_file_close()
        elif op_type == OP_FILE_READ:
            self.compile_file_read()
        elif op_type == OP_FILE_WRITE:
            self.compile_file_write()
        elif op_type == OP_FILE_APPEND:
            self.compile_file_append()

    def compile_push(self, value):
        """Compile integer push operation"""
        self.emit(f"    ; Push {value}")
        self.emit(f"    mov rax, {value}")
        self.emit("    push rax")

    def compile_push_str(self, string):
        """Compile string push operation"""
        for i, (label, s) in enumerate(self.string_literals):
            if s == string:
                str_label = label
                break
        else:
            str_label = self.add_string_literal(string)

        self.emit(f"    ; Push string \"{string}\"")
        self.emit(f"    lea rax, [{str_label}]")
        self.emit("    push rax")

    def compile_plus(self):
        """Compile addition operation"""
        self.emit("    ; Add top two values")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    add rax, rbx")
        self.emit("    push rax")

    def compile_minus(self):
        """Compile subtraction operation"""
        self.emit("    ; Subtract top from second")
        self.emit("    pop rbx")
        self.emit("    pop rax")
        self.emit("    sub rax, rbx")
        self.emit("    push rax")

    def compile_multi(self):
        """Compile multiplication operation"""
        self.emit("    ; Multiply top two values")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    imul rax, rbx")
        self.emit("    push rax")

    def compile_divide(self):
        """Compile division operation"""
        self.emit("    ; Divide second by top")
        self.emit("    pop rbx")
        self.emit("    pop rax")
        self.emit("    cqo")  # Sign-extend RAX into RDX:RAX
        self.emit("    idiv rbx")
        self.emit("    push rax")

    def compile_mod(self):
        """Compile modulo operation"""
        self.emit("    ; Modulo second by top")
        self.emit("    pop rbx")
        self.emit("    pop rax")
        self.emit("    cqo")  # Sign-extend RAX into RDX:RAX
        self.emit("    idiv rbx")
        self.emit("    push rdx")  # Remainder is in RDX

    def compile_dump(self):
        """Compile dump (print) operation"""
        self.emit("    ; Dump (print) top value")
        self.emit("    pop rdi")
        self.emit("    call print_int")

    def compile_set(self, name):
        """Compile variable set operation"""
        var_name = f"var_{len(self.variables)}"
        self.variables[name] = var_name
        self.emit(f"    ; Set variable {name}")
        self.emit(f"    {var_name} dq 0")
        self.emit("    pop rax")
        self.emit(f"    mov [{var_name}], rax")

    def compile_get(self, name):
        """Compile variable get operation"""
        if name in self.variables:
            var_name = self.variables[name]
        else:
            var_name = f"var_{len(self.variables)}"
            self.variables[name] = var_name
            self.emit(f"    {var_name} dq 0")

        self.emit(f"    ; Get variable {name}")
        self.emit(f"    mov rax, [{var_name}]")
        self.emit("    push rax")

    def compile_if(self):
        """Compile if statement"""
        label_else = self.generate_unique_label("else")
        label_endif = self.generate_unique_label("endif")
        self.if_stack.append((label_else, label_endif))

        self.emit("    ; If statement")
        self.emit("    pop rax")
        self.emit("    cmp rax, 0")
        self.emit(f"    je {label_else}")

    def compile_else(self):
        """Compile else statement"""
        if not self.if_stack:
            raise ValueError("ELSE without matching IF")

        label_else, label_endif = self.if_stack.pop()

        self.emit("    ; Else statement")
        self.emit(f"    jmp {label_endif}")
        self.emit(f"{label_else}:")

        # Push just the endif label back for ENDIF
        self.if_stack.append((None, label_endif))

    def compile_endif(self):
        """Compile endif statement"""
        if not self.if_stack:
            raise ValueError("ENDIF without matching IF")

        else_or_none, label_endif = self.if_stack.pop()

        # If there's no ELSE, we need to define the else label here
        if else_or_none is not None:
            self.emit(f"{else_or_none}:")

        self.emit("    ; End if statement")
        self.emit(f"{label_endif}:")

    def compile_greater(self):
        """Compile greater than comparison"""
        self.emit("    ; Greater than comparison")
        self.emit("    pop rbx")
        self.emit("    pop rax")
        self.emit("    cmp rax, rbx")
        self.emit("    setg al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")

    def compile_less(self):
        """Compile less than comparison"""
        self.emit("    ; Less than comparison")
        self.emit("    pop rbx")
        self.emit("    pop rax")
        self.emit("    cmp rax, rbx")
        self.emit("    setl al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")

    def compile_equal(self):
        """Compile equals comparison"""
        self.emit("    ; Equals comparison")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    cmp rax, rbx")
        self.emit("    sete al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")

    def compile_not_equal(self):
        """Compile not equals comparison"""
        self.emit("    ; Not equals comparison")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    cmp rax, rbx")
        self.emit("    setne al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")

    def compile_less_equal(self):
        """Compile less than or equal comparison"""
        self.emit("    ; Less than or equal comparison")
        self.emit("    pop rbx")
        self.emit("    pop rax")
        self.emit("    cmp rax, rbx")
        self.emit("    setle al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")

    def compile_bit_and(self):
        """Compile bitwise AND operation"""
        self.emit("    ; Bitwise AND")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    and rax, rbx")
        self.emit("    push rax")

    def compile_bit_or(self):
        """Compile bitwise OR operation"""
        self.emit("    ; Bitwise OR")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    or rax, rbx")
        self.emit("    push rax")

    def compile_bit_xor(self):
        """Compile bitwise XOR operation"""
        self.emit("    ; Bitwise XOR")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    xor rax, rbx")
        self.emit("    push rax")

    def compile_bit_not(self):
        """Compile bitwise NOT operation"""
        self.emit("    ; Bitwise NOT")
        self.emit("    pop rax")
        self.emit("    not rax")
        self.emit("    push rax")

    def compile_dup(self):
        """Compile duplicate top value operation"""
        self.emit("    ; Duplicate top value")
        self.emit("    pop rax")
        self.emit("    push rax")
        self.emit("    push rax")

    def compile_swap(self):
        """Compile swap top two values operation"""
        self.emit("    ; Swap top two values")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    push rax")
        self.emit("    push rbx")

    def compile_drop(self):
        """Compile drop top value operation"""
        self.emit("    ; Drop top value")
        self.emit("    pop rax")

    def compile_over(self):
        """Compile over operation (duplicate second item to top)"""
        self.emit("    ; Over (copy second item to top)")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    push rbx")
        self.emit("    push rax")
        self.emit("    push rbx")

    def compile_rot(self):
        """Compile rotate top three values operation"""
        self.emit("    ; Rotate top three values")
        self.emit("    pop rax")
        self.emit("    pop rbx")
        self.emit("    pop rcx")
        self.emit("    push rbx")
        self.emit("    push rax")
        self.emit("    push rcx")

    def compile_while(self):
        """Compile while loop start"""
        label_while = self.generate_unique_label("while")
        label_endwhile = self.generate_unique_label("endwhile")
        self.loop_stack.append((label_while, label_endwhile))

        self.emit("    ; While loop start")
        self.emit(f"{label_while}:")

    def compile_repeat(self):
        """Compile repeat (end of while loop)"""
        if not self.loop_stack:
            raise ValueError("REPEAT without matching WHILE")

        label_while, label_endwhile = self.loop_stack.pop()

        self.emit("    ; Check while condition")
        self.emit("    pop rax")
        self.emit("    cmp rax, 0")
        self.emit(f"    je {label_endwhile}")
        self.emit(f"    jmp {label_while}")
        self.emit(f"{label_endwhile}:")

    def compile_for(self):
        """Compile for loop start"""
        label_for = self.generate_unique_label("for")
        label_endfor = self.generate_unique_label("endfor")
        counter_var = f"for_counter_{len(self.loop_stack)}"
        end_var = f"for_end_{len(self.loop_stack)}"

        self.loop_stack.append((label_for, label_endfor, counter_var, end_var))

        self.emit("    ; For loop initialization")
        self.emit("    pop rax")  # Start value
        self.emit(f"    mov [{counter_var}], rax")
        self.emit("    pop rax")  # End value
        self.emit(f"    mov [{end_var}], rax")
        self.emit(f"{label_for}:")
        self.emit(f"    mov rax, [{counter_var}]")
        self.emit("    push rax")

    def compile_next(self):
        """Compile next (end of for loop)"""
        if not self.loop_stack:
            raise ValueError("NEXT without matching FOR")

        label_for, label_endfor, counter_var, end_var = self.loop_stack.pop()

        self.emit("    ; For loop increment and check")
        self.emit(f"    mov rax, [{counter_var}]")
        self.emit("    inc rax")
        self.emit(f"    mov [{counter_var}], rax")
        self.emit(f"    cmp rax, [{end_var}]")
        self.emit(f"    jg {label_endfor}")
        self.emit(f"    jmp {label_for}")
        self.emit(f"{label_endfor}:")

    def compile_fun_def(self, name):
        """Compile function definition"""
        if name in self.func_labels:
            label = self.func_labels[name]
            self.emit(f"    ; Function definition: {name}")
            self.emit(f"{label}:")
            self.emit("    push rbp")
            self.emit("    mov rbp, rsp")

    def compile_fun_end(self):
        """Compile function end"""
        self.emit("    ; Function end")
        self.emit("    mov rsp, rbp")
        self.emit("    pop rbp")
        self.emit("    ret")

    def compile_fun_call(self, name):
        """Compile function call"""
        if name in self.func_labels:
            label = self.func_labels[name]
            self.emit(f"    ; Function call: {name}")
            self.emit(f"    call {label}")
        else:
            raise ValueError(f"Function '{name}' not defined")

    def compile_return(self):
        """Compile return from function"""
        self.emit("    ; Return from function")
        self.emit("    mov rsp, rbp")
        self.emit("    pop rbp")
        self.emit("    ret")

    def compile_array_new(self):
        """Compile array creation"""
        self.emit("    ; Create new array")
        self.emit("    pop rax")  # Size
        self.emit("    imul rax, 8")  # Size in bytes (8 bytes per element)
        self.emit("    mov rdi, rax")
        self.emit("    call malloc")
        self.emit("    push rax")  # Push array pointer

    def compile_array_set(self):
        """Compile array set operation"""
        self.emit("    ; Set array element")
        self.emit("    pop rcx")  # Value
        self.emit("    pop rbx")  # Index
        self.emit("    pop rax")  # Array pointer
        self.emit("    imul rbx, 8")  # Index in bytes
        self.emit("    add rax, rbx")  # Address of element
        self.emit("    mov [rax], rcx")  # Set element

    def compile_array_get(self):
        """Compile array get operation"""
        self.emit("    ; Get array element")
        self.emit("    pop rbx")  # Index
        self.emit("    pop rax")  # Array pointer
        self.emit("    imul rbx, 8")  # Index in bytes
        self.emit("    add rax, rbx")  # Address of element
        self.emit("    mov rcx, [rax]")  # Get element
        self.emit("    push rcx")  # Push element

    def compile_array_len(self):
        """Compile array length operation"""
        # Since we don't track array lengths in this implementation,
        # we'll need to store them separately in a real compiler.
        self.emit("    ; Get array length (stub)")
        self.emit("    pop rax")  # Array pointer
        self.emit("    ; Real implementation would get the length")
        self.emit("    push rax")  # Push length (stub)

    def compile_str_concat(self):
        """Compile string concatenation"""
        self.emit("    ; String concatenation")
        self.emit("    pop rsi")  # Second string
        self.emit("    pop rdi")  # First string
        self.emit("    call strcat_func")
        self.emit("    push rax")  # Push result

    def compile_str_length(self):
        """Compile string length operation"""
        self.emit("    ; String length")
        self.emit("    pop rdi")  # String
        self.emit("    call strlen")
        self.emit("    push rax")  # Push length

    def compile_str_slice(self):
        """Compile string slice operation"""
        self.emit("    ; String slice")
        self.emit("    pop rdx")  # End
        self.emit("    pop rcx")  # Start
        self.emit("    pop rsi")  # String
        self.emit("    call substr_func")
        self.emit("    push rax")  # Push result

    def compile_str_contains(self):
        """Compile string contains operation"""
        self.emit("    ; String contains")
        self.emit("    pop rdi")  # Substring
        self.emit("    pop rsi")  # String
        self.emit("    call strstr")
        self.emit("    cmp rax, 0")
        self.emit("    setne al")
        self.emit("    movzx rax, al")
        self.emit("    push rax")  # Push result (1 if found, 0 if not)

    def compile_str_split(self):
        """Compile string split operation"""
        self.emit("    ; String split")
        self.emit("    pop rdi")  # Delimiter
        self.emit("    pop rsi")  # String
        self.emit("    call str_split_func")
        self.emit("    push rax")  # Push result array

    def compile_str(self):
        """Compile integer to string conversion"""
        self.emit("    ; Integer to string conversion")
        self.emit("    pop rdi")  # Integer
        self.emit("    call int_to_str_func")
        self.emit("    push rax")  # Push result string

    def compile_file_open(self):
        """Compile file open operation"""
        self.emit("    ; File open")
        self.emit("    pop rsi")  # Mode
        self.emit("    pop rdi")  # Filename
        self.emit("    call fopen")
        self.emit("    cmp rax, 0")
        self.emit("    je file_error")
        self.emit("    push rax")  # Push file handle

    def compile_file_close(self):
        """Compile file close operation"""
        self.emit("    ; File close")
        self.emit("    pop rdi")  # File handle
        self.emit("    call fclose")

    def compile_file_read(self):
        """Compile file read operation"""
        self.emit("    ; File read")
        self.emit("    pop rdi")  # File handle
        self.emit("    call file_read_func")
        self.emit("    push rax")  # Push content

    def compile_file_write(self):
        """Compile file write operation"""
        self.emit("    ; File write")
        self.emit("    pop rsi")  # Content
        self.emit("    pop rdi")  # File handle
        self.emit("    call file_write_func")

    def compile_file_append(self):
        """Compile file append operation"""
        self.emit("    ; File append")
        self.emit("    pop rsi")  # Content
        self.emit("    pop rdi")  # File handle
        self.emit("    call file_append_func")