
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TOKEN_LENGTH 256
#define MAX_PROGRAM_SIZE 10000
#define MAX_VARS 1000

typedef enum {
    OP_PUSH,
    OP_PUSH_STR,
    OP_PLUS,
    OP_MINUS,
    OP_MULTI,
    OP_DIVIDE,
    OP_MOD,
    OP_DUMP,
    OP_DUP,
    OP_SWAP,
    OP_DROP,
    OP_SET_VAR,
    OP_GET_VAR,
    OP_IF,
    OP_ELSE,
    OP_ENDIF,
    OP_WHILE,
    OP_REPEAT,
    // Add other operations as needed
} OpCode;

typedef struct {
    OpCode code;
    int int_value;
    char *str_value;
} Operation;

Operation program[MAX_PROGRAM_SIZE];
int program_size = 0;

// Function to add an operation to the program
void add_operation(OpCode code, int int_value, const char *str_value) {
    if (program_size >= MAX_PROGRAM_SIZE) {
        fprintf(stderr, "Error: Program too large\n");
        exit(1);
    }
    
    program[program_size].code = code;
    program[program_size].int_value = int_value;
    
    if (str_value) {
        program[program_size].str_value = strdup(str_value);
    } else {
        program[program_size].str_value = NULL;
    }
    
    program_size++;
}

// Parse a Backstack program from a file
void parse_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        exit(1);
    }
    
    char line[MAX_TOKEN_LENGTH];
    while (fgets(line, sizeof(line), file)) {
        // Remove newline
        size_t len = strlen(line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
        }
        
        // Skip empty lines and comments
        if (line[0] == '\0' || line[0] == '#') {
            continue;
        }
        
        // Remove inline comments
        char *comment = strchr(line, '#');
        if (comment) {
            *comment = '\0';
        }
        
        // Trim whitespace
        char *p = line;
        while (isspace(*p)) p++;
        
        if (*p == '\0') continue; // Skip empty lines after trimming
        
        // Process tokens in the line
        if (*p == '"') {
            // String literal
            p++; // Skip opening quote
            char *end = strchr(p, '"');
            if (end) {
                *end = '\0';
                add_operation(OP_PUSH_STR, 0, p);
            }
        } else if (isdigit(*p) || (*p == '-' && isdigit(*(p+1)))) {
            // Number
            int value = atoi(p);
            add_operation(OP_PUSH, value, NULL);
        } else if (strcmp(p, "+") == 0) {
            add_operation(OP_PLUS, 0, NULL);
        } else if (strcmp(p, "-") == 0) {
            add_operation(OP_MINUS, 0, NULL);
        } else if (strcmp(p, "*") == 0) {
            add_operation(OP_MULTI, 0, NULL);
        } else if (strcmp(p, "/") == 0) {
            add_operation(OP_DIVIDE, 0, NULL);
        } else if (strcmp(p, "%") == 0) {
            add_operation(OP_MOD, 0, NULL);
        } else if (strcmp(p, "dump") == 0) {
            add_operation(OP_DUMP, 0, NULL);
        } else if (strcmp(p, "dup") == 0) {
            add_operation(OP_DUP, 0, NULL);
        } else if (strcmp(p, "swap") == 0) {
            add_operation(OP_SWAP, 0, NULL);
        } else if (strcmp(p, "drop") == 0) {
            add_operation(OP_DROP, 0, NULL);
        } else if (strncmp(p, "set:", 4) == 0) {
            add_operation(OP_SET_VAR, 0, p + 4);
        } else if (strncmp(p, "get:", 4) == 0) {
            add_operation(OP_GET_VAR, 0, p + 4);
        } else if (strcmp(p, "if") == 0) {
            add_operation(OP_IF, 0, NULL);
        } else if (strcmp(p, "else") == 0) {
            add_operation(OP_ELSE, 0, NULL);
        } else if (strcmp(p, "endif") == 0) {
            add_operation(OP_ENDIF, 0, NULL);
        } else if (strcmp(p, "while") == 0) {
            add_operation(OP_WHILE, 0, NULL);
        } else if (strcmp(p, "repeat") == 0) {
            add_operation(OP_REPEAT, 0, NULL);
        }
        // Add other operations as needed
    }
    
    fclose(file);
}

// Simulate a Backstack program (interpreter)
void simulate_program() {
    int stack[1000];
    int stack_size = 0;
    char *var_names[MAX_VARS];
    int var_values[MAX_VARS];
    int var_count = 0;
    
    int pc = 0;
    while (pc < program_size) {
        Operation op = program[pc];
        
        switch (op.code) {
            case OP_PUSH:
                stack[stack_size++] = op.int_value;
                break;
                
            case OP_PUSH_STR:
                // This is simplified - in a real implementation we'd need to handle strings properly
                printf("String operation not fully implemented: %s\n", op.str_value);
                break;
                
            case OP_PLUS:
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                stack[stack_size-2] = stack[stack_size-2] + stack[stack_size-1];
                stack_size--;
                break;
                
            case OP_MINUS:
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                stack[stack_size-2] = stack[stack_size-2] - stack[stack_size-1];
                stack_size--;
                break;
                
            case OP_MULTI:
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                stack[stack_size-2] = stack[stack_size-2] * stack[stack_size-1];
                stack_size--;
                break;
                
            case OP_DIVIDE:
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                if (stack[stack_size-1] == 0) {
                    fprintf(stderr, "Error: Division by zero\n");
                    exit(1);
                }
                stack[stack_size-2] = stack[stack_size-2] / stack[stack_size-1];
                stack_size--;
                break;
                
            case OP_MOD:
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                if (stack[stack_size-1] == 0) {
                    fprintf(stderr, "Error: Division by zero\n");
                    exit(1);
                }
                stack[stack_size-2] = stack[stack_size-2] % stack[stack_size-1];
                stack_size--;
                break;
                
            case OP_DUMP:
                if (stack_size < 1) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                printf("%d\n", stack[stack_size-1]);
                stack_size--;
                break;
                
            case OP_DUP:
                if (stack_size < 1) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                stack[stack_size] = stack[stack_size-1];
                stack_size++;
                break;
                
            case OP_SWAP:
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                int temp = stack[stack_size-1];
                stack[stack_size-1] = stack[stack_size-2];
                stack[stack_size-2] = temp;
                break;
                
            case OP_DROP:
                if (stack_size < 1) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                stack_size--;
                break;
                
            case OP_SET_VAR:
                if (stack_size < 1) {
                    fprintf(stderr, "Error: Stack underflow\n");
                    exit(1);
                }
                // Find existing variable or create new one
                {
                    int i;
                    for (i = 0; i < var_count; i++) {
                        if (strcmp(var_names[i], op.str_value) == 0) {
                            var_values[i] = stack[--stack_size];
                            break;
                        }
                    }
                    if (i == var_count) {
                        if (var_count >= MAX_VARS) {
                            fprintf(stderr, "Error: Too many variables\n");
                            exit(1);
                        }
                        var_names[var_count] = strdup(op.str_value);
                        var_values[var_count] = stack[--stack_size];
                        var_count++;
                    }
                }
                break;
                
            case OP_GET_VAR:
                // Find variable
                {
                    int i;
                    for (i = 0; i < var_count; i++) {
                        if (strcmp(var_names[i], op.str_value) == 0) {
                            stack[stack_size++] = var_values[i];
                            break;
                        }
                    }
                    if (i == var_count) {
                        fprintf(stderr, "Error: Variable '%s' not found\n", op.str_value);
                        exit(1);
                    }
                }
                break;
                
            // Implement other operations as needed
                
            default:
                fprintf(stderr, "Error: Unknown operation code %d\n", op.code);
                exit(1);
        }
        
        pc++;
    }
}

// Compile a Backstack program to assembly
void compile_program_to_asm(const char *output_file) {
    FILE *out = fopen(output_file, "w");
    if (!out) {
        fprintf(stderr, "Error: Cannot open output file %s\n", output_file);
        exit(1);
    }
    
    // Basic x86-64 assembly setup
    fprintf(out, "section .text\n");
    fprintf(out, "global _start\n");
    fprintf(out, "_start:\n");
    
    // Data section for strings and other data
    fprintf(out, "section .data\n");
    fprintf(out, "fmt db \"%%d\", 10, 0\n");
    
    // Variables section
    fprintf(out, "section .bss\n");
    
    // Close file
    fclose(out);
    
    printf("Compilation to assembly not fully implemented yet\n");
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <cmd> <filename>\n", argv[0]);
        fprintf(stderr, "  cmd: sim (simulate) or com (compile)\n");
        return 1;
    }
    
    parse_file(argv[2]);
    
    if (strcmp(argv[1], "sim") == 0) {
        simulate_program();
    } else if (strcmp(argv[1], "com") == 0) {
        compile_program_to_asm("output.asm");
        // You would then call the assembler and linker here
        system("nasm -felf64 output.asm -o output.o");
        system("ld output.o -o backstack.exe");
    } else {
        fprintf(stderr, "Unknown command: %s\n", argv[1]);
        return 1;
    }
    
    return 0;
}
