
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define MAX_TOKEN_LENGTH 256
#define MAX_PROGRAM_SIZE 10000
#define MAX_VARS 1000
#define MAX_STACK_SIZE 1000
#define MAX_STRING_SIZE 4096
#define MAX_FUNCTIONS 100
#define MAX_ARRAY_SIZE 1000
#define MAX_FILES 10

typedef enum {
    OP_PUSH,
    OP_PUSH_STR,
    OP_PLUS,
    OP_MINUS,
    OP_MULTI,
    OP_DIVIDE,
    OP_MOD,
    OP_EXPO,
    OP_FLOOR,
    OP_BIT_AND,
    OP_BIT_OR,
    OP_BIT_XOR,
    OP_BIT_NOT,
    OP_BIT_SHIFT_LEFT,
    OP_BIT_SHIFT_RIGHT,
    OP_EQUAL,
    OP_NOT_EQUAL,
    OP_GREATER,
    OP_LESS,
    OP_LESS_EQUAL,
    OP_GREATER_EQUAL,
    OP_IF,
    OP_ELSE,
    OP_ENDIF,
    OP_WHILE,
    OP_REPEAT,
    OP_FOR,
    OP_NEXT,
    OP_DUP,
    OP_SWAP,
    OP_DROP,
    OP_OVER,
    OP_ROT,
    OP_DUMP,
    OP_SET_VAR,
    OP_GET_VAR,
    OP_ARRAY_NEW,
    OP_ARRAY_SET,
    OP_ARRAY_GET,
    OP_ARRAY_LEN,
    OP_STR_CONCAT,
    OP_STR_LENGTH,
    OP_STR_SLICE,
    OP_STR_CONTAINS,
    OP_STR_SPLIT,
    OP_STR,
    OP_INPUT,
    OP_INPUT_INT,
    OP_FILE_OPEN,
    OP_FILE_CLOSE,
    OP_FILE_READ,
    OP_FILE_WRITE,
    OP_FILE_APPEND,
    OP_FUN_DEF,
    OP_FUN_END,
    OP_FUN_CALL,
    OP_RETURN
} OpCode;

typedef enum {
    TYPE_INT,
    TYPE_STRING,
    TYPE_ARRAY_ID
} ValueType;

typedef struct {
    ValueType type;
    union {
        int int_value;
        char *str_value;
        int array_id;
    } value;
} StackValue;

typedef struct {
    OpCode code;
    int int_value;
    char *str_value;
} Operation;

typedef struct {
    char *name;
    int position;
} Function;

typedef struct {
    StackValue *elements;
    int size;
} Array;

// Global variables
Operation program[MAX_PROGRAM_SIZE];
int program_size = 0;
StackValue stack[MAX_STACK_SIZE];
int stack_size = 0;
char *var_names[MAX_VARS];
StackValue var_values[MAX_VARS];
int var_count = 0;
Function functions[MAX_FUNCTIONS];
int function_count = 0;
int if_stack[100];
int if_stack_size = 0;
int loop_stack[100];
int loop_stack_size = 0;
int call_stack[100];
int call_stack_size = 0;
Array arrays[MAX_ARRAY_SIZE];
int array_count = 0;
FILE *open_files[MAX_FILES] = {NULL};

// Forward declarations
void simulate_program(int debug);
void print_stack_value(StackValue value);

// Helper functions for stack values
StackValue make_int_value(int value) {
    StackValue sv;
    sv.type = TYPE_INT;
    sv.value.int_value = value;
    return sv;
}

StackValue make_string_value(const char *value) {
    StackValue sv;
    sv.type = TYPE_STRING;
    sv.value.str_value = strdup(value);
    return sv;
}

StackValue make_array_id_value(int array_id) {
    StackValue sv;
    sv.type = TYPE_ARRAY_ID;
    sv.value.array_id = array_id;
    return sv;
}

void free_stack_value(StackValue *value) {
    if (value->type == TYPE_STRING && value->value.str_value != NULL) {
        free(value->value.str_value);
        value->value.str_value = NULL;
    }
}

// Stack operations
void push_stack(StackValue value) {
    if (stack_size >= MAX_STACK_SIZE) {
        fprintf(stderr, "Error: Stack overflow\n");
        exit(1);
    }
    stack[stack_size++] = value;
}

StackValue pop_stack() {
    if (stack_size <= 0) {
        fprintf(stderr, "Error: Stack underflow\n");
        exit(1);
    }
    return stack[--stack_size];
}

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
        
        // Trim trailing whitespace
        char *end = p + strlen(p) - 1;
        while(end > p && isspace(*end)) end--;
        *(end + 1) = '\0';
        
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
        } else if (strcmp(p, "^") == 0) {
            add_operation(OP_EXPO, 0, NULL);
        } else if (strcmp(p, "//") == 0) {
            add_operation(OP_FLOOR, 0, NULL);
        } else if (strcmp(p, "&") == 0) {
            add_operation(OP_BIT_AND, 0, NULL);
        } else if (strcmp(p, "|") == 0) {
            add_operation(OP_BIT_OR, 0, NULL);
        } else if (strcmp(p, "^") == 0) {
            add_operation(OP_BIT_XOR, 0, NULL);
        } else if (strcmp(p, "~") == 0) {
            add_operation(OP_BIT_NOT, 0, NULL);
        } else if (strcmp(p, "<<") == 0) {
            add_operation(OP_BIT_SHIFT_LEFT, 0, NULL);
        } else if (strcmp(p, ">>") == 0) {
            add_operation(OP_BIT_SHIFT_RIGHT, 0, NULL);
        } else if (strcmp(p, "==") == 0) {
            add_operation(OP_EQUAL, 0, NULL);
        } else if (strcmp(p, "!=") == 0) {
            add_operation(OP_NOT_EQUAL, 0, NULL);
        } else if (strcmp(p, ">") == 0) {
            add_operation(OP_GREATER, 0, NULL);
        } else if (strcmp(p, "<") == 0) {
            add_operation(OP_LESS, 0, NULL);
        } else if (strcmp(p, "<=") == 0) {
            add_operation(OP_LESS_EQUAL, 0, NULL);
        } else if (strcmp(p, ">=") == 0) {
            add_operation(OP_GREATER_EQUAL, 0, NULL);
        } else if (strcmp(p, "dump") == 0) {
            add_operation(OP_DUMP, 0, NULL);
        } else if (strcmp(p, "dup") == 0) {
            add_operation(OP_DUP, 0, NULL);
        } else if (strcmp(p, "swap") == 0) {
            add_operation(OP_SWAP, 0, NULL);
        } else if (strcmp(p, "drop") == 0) {
            add_operation(OP_DROP, 0, NULL);
        } else if (strcmp(p, "over") == 0) {
            add_operation(OP_OVER, 0, NULL);
        } else if (strcmp(p, "rot") == 0) {
            add_operation(OP_ROT, 0, NULL);
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
        } else if (strcmp(p, "for") == 0) {
            add_operation(OP_FOR, 0, NULL);
        } else if (strcmp(p, "next") == 0) {
            add_operation(OP_NEXT, 0, NULL);
        } else if (strncmp(p, "set:", 4) == 0) {
            add_operation(OP_SET_VAR, 0, p + 4);
        } else if (strncmp(p, "get:", 4) == 0) {
            add_operation(OP_GET_VAR, 0, p + 4);
        } else if (strcmp(p, "array_new") == 0) {
            add_operation(OP_ARRAY_NEW, 0, NULL);
        } else if (strcmp(p, "array_set") == 0) {
            add_operation(OP_ARRAY_SET, 0, NULL);
        } else if (strcmp(p, "array_get") == 0) {
            add_operation(OP_ARRAY_GET, 0, NULL);
        } else if (strcmp(p, "array_len") == 0) {
            add_operation(OP_ARRAY_LEN, 0, NULL);
        } else if (strcmp(p, "str_concat") == 0) {
            add_operation(OP_STR_CONCAT, 0, NULL);
        } else if (strcmp(p, "str_length") == 0) {
            add_operation(OP_STR_LENGTH, 0, NULL);
        } else if (strcmp(p, "str_slice") == 0) {
            add_operation(OP_STR_SLICE, 0, NULL);
        } else if (strcmp(p, "str_contains") == 0) {
            add_operation(OP_STR_CONTAINS, 0, NULL);
        } else if (strcmp(p, "str_split") == 0) {
            add_operation(OP_STR_SPLIT, 0, NULL);
        } else if (strcmp(p, "str") == 0) {
            add_operation(OP_STR, 0, NULL);
        } else if (strcmp(p, "input") == 0) {
            add_operation(OP_INPUT, 0, NULL);
        } else if (strcmp(p, "input_int") == 0) {
            add_operation(OP_INPUT_INT, 0, NULL);
        } else if (strcmp(p, "file_open") == 0) {
            add_operation(OP_FILE_OPEN, 0, NULL);
        } else if (strcmp(p, "file_close") == 0) {
            add_operation(OP_FILE_CLOSE, 0, NULL);
        } else if (strcmp(p, "file_read") == 0) {
            add_operation(OP_FILE_READ, 0, NULL);
        } else if (strcmp(p, "file_write") == 0) {
            add_operation(OP_FILE_WRITE, 0, NULL);
        } else if (strcmp(p, "file_append") == 0) {
            add_operation(OP_FILE_APPEND, 0, NULL);
        } else if (strncmp(p, "fun:", 4) == 0) {
            add_operation(OP_FUN_DEF, 0, p + 4);
        } else if (strcmp(p, "fun_end") == 0) {
            add_operation(OP_FUN_END, 0, NULL);
        } else if (strncmp(p, "call:", 5) == 0) {
            add_operation(OP_FUN_CALL, 0, p + 5);
        } else if (strcmp(p, "return") == 0) {
            add_operation(OP_RETURN, 0, NULL);
        } else {
            fprintf(stderr, "Error: Unknown token '%s'\n", p);
            exit(1);
        }
    }
    
    fclose(file);
}

// Pre-process functions
void preprocess_functions(int debug) {
    if (debug) {
        printf("DEBUG: Pre-processing function definitions...\n");
    }
    
    for (int pc = 0; pc < program_size; pc++) {
        if (program[pc].code == OP_FUN_DEF) {
            const char *fun_name = program[pc].str_value;
            
            // Store function position (after FUN_DEF)
            if (function_count >= MAX_FUNCTIONS) {
                fprintf(stderr, "Error: Too many functions\n");
                exit(1);
            }
            
            functions[function_count].name = strdup(fun_name);
            functions[function_count].position = pc + 1;
            
            if (debug) {
                printf("DEBUG: Pre-registered function '%s' at position %d\n", 
                       fun_name, pc + 1);
            }
            
            function_count++;
        }
    }
}

// Simulate a Backstack program (interpreter)
void simulate_program(int debug) {
    // Initialize arrays
    for (int i = 0; i < MAX_ARRAY_SIZE; i++) {
        arrays[i].elements = NULL;
        arrays[i].size = 0;
    }
    
    // Initialize call stack, loop stack, if stack
    call_stack_size = 0;
    loop_stack_size = 0;
    if_stack_size = 0;
    
    // Pre-process functions
    preprocess_functions(debug);
    
    // Initialize variables for program execution
    int pc = 0;          // Program counter
    int skip_mode = 0;   // For handling conditional branches
    
    // Main execution loop
    while (pc < program_size) {
        Operation op = program[pc];
        
        // Handle IF/ELSE/ENDIF when in skip mode
        if (skip_mode) {
            if (op.code == OP_IF) {
                if_stack[if_stack_size++] = 0;  // Track nested if when skipping
            } else if (op.code == OP_ELSE) {
                if (if_stack_size > 0 && if_stack[if_stack_size-1] == 0) {
                    skip_mode = 0;  // Exit skip mode at matching else
                    if_stack_size--;
                }
            } else if (op.code == OP_ENDIF) {
                if (if_stack_size > 0) {
                    if_stack_size--;  // Pop nested if
                    if (if_stack_size == 0) {
                        skip_mode = 0;  // Exit skip mode at endif
                    }
                } else {
                    skip_mode = 0;  // Exit skip mode at endif
                }
            }
            
            pc++;
            continue;
        }
        
        // Normal operation execution
        switch (op.code) {
            case OP_PUSH: {
                push_stack(make_int_value(op.int_value));
                break;
            }
            
            case OP_PUSH_STR: {
                push_stack(make_string_value(op.str_value));
                break;
            }
            
            case OP_PLUS: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value + b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Addition requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_MINUS: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value - b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Subtraction requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_MULTI: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value * b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Multiplication requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_DIVIDE: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    if (b.value.int_value == 0) {
                        fprintf(stderr, "Error: Division by zero\n");
                        exit(1);
                    }
                    push_stack(make_int_value(a.value.int_value / b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Division requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_MOD: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    if (b.value.int_value == 0) {
                        fprintf(stderr, "Error: Modulo by zero\n");
                        exit(1);
                    }
                    push_stack(make_int_value(a.value.int_value % b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Modulo requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_EXPO: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    int result = 1;
                    for (int i = 0; i < b.value.int_value; i++) {
                        result *= a.value.int_value;
                    }
                    push_stack(make_int_value(result));
                } else {
                    fprintf(stderr, "Error: Exponentiation requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_FLOOR: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    if (b.value.int_value == 0) {
                        fprintf(stderr, "Error: Floor division by zero\n");
                        exit(1);
                    }
                    push_stack(make_int_value(a.value.int_value / b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Floor division requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_BIT_AND: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value & b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Bitwise AND requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_BIT_OR: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value | b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Bitwise OR requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_BIT_XOR: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value ^ b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Bitwise XOR requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_BIT_NOT: {
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT) {
                    push_stack(make_int_value(~a.value.int_value));
                } else {
                    fprintf(stderr, "Error: Bitwise NOT requires an integer\n");
                    exit(1);
                }
                break;
            }
            
            case OP_BIT_SHIFT_LEFT: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value << b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Bitwise shift left requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_BIT_SHIFT_RIGHT: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value >> b.value.int_value));
                } else {
                    fprintf(stderr, "Error: Bitwise shift right requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_EQUAL: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value == b.value.int_value ? 1 : 0));
                } else if (a.type == TYPE_STRING && b.type == TYPE_STRING) {
                    push_stack(make_int_value(strcmp(a.value.str_value, b.value.str_value) == 0 ? 1 : 0));
                } else {
                    fprintf(stderr, "Error: Equality check requires same types\n");
                    exit(1);
                }
                free_stack_value(&a);
                free_stack_value(&b);
                break;
            }
            
            case OP_NOT_EQUAL: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value != b.value.int_value ? 1 : 0));
                } else if (a.type == TYPE_STRING && b.type == TYPE_STRING) {
                    push_stack(make_int_value(strcmp(a.value.str_value, b.value.str_value) != 0 ? 1 : 0));
                } else {
                    fprintf(stderr, "Error: Inequality check requires same types\n");
                    exit(1);
                }
                free_stack_value(&a);
                free_stack_value(&b);
                break;
            }
            
            case OP_GREATER: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value > b.value.int_value ? 1 : 0));
                } else {
                    fprintf(stderr, "Error: Greater than check requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_LESS: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value < b.value.int_value ? 1 : 0));
                } else {
                    fprintf(stderr, "Error: Less than check requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_LESS_EQUAL: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value <= b.value.int_value ? 1 : 0));
                } else {
                    fprintf(stderr, "Error: Less than or equal check requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_GREATER_EQUAL: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    push_stack(make_int_value(a.value.int_value >= b.value.int_value ? 1 : 0));
                } else {
                    fprintf(stderr, "Error: Greater than or equal check requires two integers\n");
                    exit(1);
                }
                break;
            }
            
            case OP_IF: {
                StackValue condition = pop_stack();
                
                if (condition.type != TYPE_INT) {
                    fprintf(stderr, "Error: IF condition must be an integer\n");
                    exit(1);
                }
                
                if (condition.value.int_value == 0) {  // False
                    skip_mode = 1;
                    if_stack[if_stack_size++] = 1;  // Mark this if as active
                } else {
                    if_stack[if_stack_size++] = 0;  // Not skipping but track for nesting
                }
                break;
            }
            
            case OP_ELSE: {
                if (if_stack_size == 0) {
                    fprintf(stderr, "Error: ELSE without matching IF\n");
                    exit(1);
                }
                
                if (if_stack[if_stack_size-1] == 0) {  // We didn't skip the IF part
                    skip_mode = 1;  // Skip the ELSE part
                }
                if_stack_size--;  // Pop the current if
                if_stack[if_stack_size++] = !skip_mode;  // Track for nested if
                break;
            }
            
            case OP_ENDIF: {
                if (if_stack_size == 0) {
                    fprintf(stderr, "Error: ENDIF without matching IF\n");
                    exit(1);
                }
                if_stack_size--;  // Pop the current if state
                if (if_stack_size == 0) {
                    skip_mode = 0;  // Reset skip mode at the outermost endif
                }
                break;
            }
            
            case OP_WHILE: {
                // Mark loop start for REPEAT to jump back to
                loop_stack[loop_stack_size++] = pc;
                break;
            }
            
            case OP_REPEAT: {
                StackValue condition = pop_stack();
                
                if (condition.type != TYPE_INT) {
                    fprintf(stderr, "Error: REPEAT condition must be an integer\n");
                    exit(1);
                }
                
                if (condition.value.int_value != 0) {  // True, continue loop
                    if (loop_stack_size == 0) {
                        fprintf(stderr, "Error: REPEAT without matching WHILE\n");
                        exit(1);
                    }
                    pc = loop_stack[loop_stack_size-1];  // Jump back to WHILE
                } else {
                    // Exit the loop
                    if (loop_stack_size > 0) {
                        loop_stack_size--;
                    }
                }
                break;
            }
            
            case OP_FOR: {
                StackValue start = pop_stack();
                StackValue end = pop_stack();
                
                if (start.type != TYPE_INT || end.type != TYPE_INT) {
                    fprintf(stderr, "Error: FOR loop requires integer values\n");
                    exit(1);
                }
                
                // Store loop counter in variables
                int var_idx = -1;
                for (int i = 0; i < var_count; i++) {
                    if (strcmp(var_names[i], "_loop_counter") == 0) {
                        var_idx = i;
                        break;
                    }
                }
                
                if (var_idx == -1) {
                    // Create new variable
                    if (var_count >= MAX_VARS) {
                        fprintf(stderr, "Error: Too many variables\n");
                        exit(1);
                    }
                    var_names[var_count] = strdup("_loop_counter");
                    var_values[var_count] = start;
                    var_count++;
                } else {
                    // Update existing variable
                    var_values[var_idx] = start;
                }
                
                // Save end value
                var_idx = -1;
                for (int i = 0; i < var_count; i++) {
                    if (strcmp(var_names[i], "_loop_end") == 0) {
                        var_idx = i;
                        break;
                    }
                }
                
                if (var_idx == -1) {
                    // Create new variable
                    if (var_count >= MAX_VARS) {
                        fprintf(stderr, "Error: Too many variables\n");
                        exit(1);
                    }
                    var_names[var_count] = strdup("_loop_end");
                    var_values[var_count] = end;
                    var_count++;
                } else {
                    // Update existing variable
                    var_values[var_idx] = end;
                }
                
                // Mark loop start for NEXT
                loop_stack[loop_stack_size++] = pc;
                
                // Push start value to stack
                push_stack(start);
                break;
            }
            
            case OP_NEXT: {
                // Find loop variables
                int counter_idx = -1;
                int end_idx = -1;
                
                for (int i = 0; i < var_count; i++) {
                    if (strcmp(var_names[i], "_loop_counter") == 0) {
                        counter_idx = i;
                    } else if (strcmp(var_names[i], "_loop_end") == 0) {
                        end_idx = i;
                    }
                }
                
                if (counter_idx == -1 || end_idx == -1 || loop_stack_size == 0) {
                    fprintf(stderr, "Error: NEXT without proper FOR setup\n");
                    exit(1);
                }
                
                // Increment counter
                var_values[counter_idx].value.int_value++;
                
                // Check if loop should continue
                if (var_values[counter_idx].value.int_value <= var_values[end_idx].value.int_value) {
                    // Push current counter to stack
                    push_stack(var_values[counter_idx]);
                    
                    // Jump back to the matching FOR
                    pc = loop_stack[loop_stack_size-1];
                } else {
                    // Exit the loop
                    loop_stack_size--;
                }
                break;
            }
            
            case OP_DUP: {
                if (stack_size == 0) {
                    fprintf(stderr, "Error: Stack underflow in DUP\n");
                    exit(1);
                }
                
                StackValue val = stack[stack_size-1];
                if (val.type == TYPE_STRING) {
                    push_stack(make_string_value(val.value.str_value));
                } else {
                    push_stack(val);
                }
                break;
            }
            
            case OP_SWAP: {
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow in SWAP\n");
                    exit(1);
                }
                
                StackValue tmp = stack[stack_size-1];
                stack[stack_size-1] = stack[stack_size-2];
                stack[stack_size-2] = tmp;
                break;
            }
            
            case OP_DROP: {
                if (stack_size == 0) {
                    fprintf(stderr, "Error: Stack underflow in DROP\n");
                    exit(1);
                }
                
                StackValue val = pop_stack();
                free_stack_value(&val);
                break;
            }
            
            case OP_OVER: {
                if (stack_size < 2) {
                    fprintf(stderr, "Error: Stack underflow in OVER\n");
                    exit(1);
                }
                
                StackValue val = stack[stack_size-2];
                if (val.type == TYPE_STRING) {
                    push_stack(make_string_value(val.value.str_value));
                } else {
                    push_stack(val);
                }
                break;
            }
            
            case OP_ROT: {
                if (stack_size < 3) {
                    fprintf(stderr, "Error: Stack underflow in ROT\n");
                    exit(1);
                }
                
                StackValue a = stack[stack_size-3];
                StackValue b = stack[stack_size-2];
                StackValue c = stack[stack_size-1];
                
                stack[stack_size-3] = b;
                stack[stack_size-2] = c;
                stack[stack_size-1] = a;
                break;
            }
            
            case OP_DUMP: {
                if (stack_size == 0) {
                    fprintf(stderr, "Error: Stack underflow in DUMP\n");
                    exit(1);
                }
                
                StackValue val = pop_stack();
                print_stack_value(val);
                free_stack_value(&val);
                break;
            }
            
            case OP_SET_VAR: {
                if (stack_size == 0) {
                    fprintf(stderr, "Error: Stack underflow in SET_VAR\n");
                    exit(1);
                }
                
                StackValue val = pop_stack();
                const char *var_name = op.str_value;
                
                // Check if variable already exists
                int i;
                for (i = 0; i < var_count; i++) {
                    if (strcmp(var_names[i], var_name) == 0) {
                        // Free old value if it's a string
                        free_stack_value(&var_values[i]);
                        // Update existing variable
                        var_values[i] = val;
                        break;
                    }
                }
                
                if (i == var_count) {
                    // Create new variable
                    if (var_count >= MAX_VARS) {
                        fprintf(stderr, "Error: Too many variables\n");
                        exit(1);
                    }
                    var_names[var_count] = strdup(var_name);
                    var_values[var_count] = val;
                    var_count++;
                }
                break;
            }
            
            case OP_GET_VAR: {
                const char *var_name = op.str_value;
                
                // Find variable
                int i;
                for (i = 0; i < var_count; i++) {
                    if (strcmp(var_names[i], var_name) == 0) {
                        // Push variable value to stack
                        if (var_values[i].type == TYPE_STRING) {
                            push_stack(make_string_value(var_values[i].value.str_value));
                        } else {
                            push_stack(var_values[i]);
                        }
                        break;
                    }
                }
                
                if (i == var_count) {
                    fprintf(stderr, "Error: Variable '%s' not found\n", var_name);
                    exit(1);
                }
                break;
            }
            
            case OP_ARRAY_NEW: {
                StackValue size_val = pop_stack();
                
                if (size_val.type != TYPE_INT) {
                    fprintf(stderr, "Error: Array size must be an integer\n");
                    exit(1);
                }
                
                int size = size_val.value.int_value;
                if (size < 0) {
                    fprintf(stderr, "Error: Array size cannot be negative\n");
                    exit(1);
                }
                
                int array_id = array_count++;
                arrays[array_id].elements = malloc(size * sizeof(StackValue));
                arrays[array_id].size = size;
                
                // Initialize array elements to 0
                for (int i = 0; i < size; i++) {
                    arrays[array_id].elements[i] = make_int_value(0);
                }
                
                push_stack(make_array_id_value(array_id));
                break;
            }
            
            case OP_ARRAY_SET: {
                StackValue value = pop_stack();
                StackValue index_val = pop_stack();
                StackValue array_id_val = pop_stack();
                
                if (index_val.type != TYPE_INT || array_id_val.type != TYPE_ARRAY_ID) {
                    fprintf(stderr, "Error: Array index and ID must be integers\n");
                    exit(1);
                }
                
                int index = index_val.value.int_value;
                int array_id = array_id_val.value.array_id;
                
                if (array_id < 0 || array_id >= array_count) {
                    fprintf(stderr, "Error: Invalid array ID: %d\n", array_id);
                    exit(1);
                }
                
                if (index < 0 || index >= arrays[array_id].size) {
                    fprintf(stderr, "Error: Array index out of bounds: %d\n", index);
                    exit(1);
                }
                
                // Free old value if it's a string
                free_stack_value(&arrays[array_id].elements[index]);
                
                // Set new value
                arrays[array_id].elements[index] = value;
                break;
            }
            
            case OP_ARRAY_GET: {
                StackValue index_val = pop_stack();
                StackValue array_id_val = pop_stack();
                
                if (index_val.type != TYPE_INT || array_id_val.type != TYPE_ARRAY_ID) {
                    fprintf(stderr, "Error: Array index and ID must be integers\n");
                    exit(1);
                }
                
                int index = index_val.value.int_value;
                int array_id = array_id_val.value.array_id;
                
                if (array_id < 0 || array_id >= array_count) {
                    fprintf(stderr, "Error: Invalid array ID: %d\n", array_id);
                    exit(1);
                }
                
                if (index < 0 || index >= arrays[array_id].size) {
                    fprintf(stderr, "Error: Array index out of bounds: %d\n", index);
                    exit(1);
                }
                
                // Get value
                StackValue value = arrays[array_id].elements[index];
                if (value.type == TYPE_STRING) {
                    push_stack(make_string_value(value.value.str_value));
                } else {
                    push_stack(value);
                }
                break;
            }
            
            case OP_ARRAY_LEN: {
                StackValue array_id_val = pop_stack();
                
                if (array_id_val.type != TYPE_ARRAY_ID) {
                    fprintf(stderr, "Error: Expected array ID\n");
                    exit(1);
                }
                
                int array_id = array_id_val.value.array_id;
                
                if (array_id < 0 || array_id >= array_count) {
                    fprintf(stderr, "Error: Invalid array ID: %d\n", array_id);
                    exit(1);
                }
                
                push_stack(make_int_value(arrays[array_id].size));
                break;
            }
            
            case OP_STR_CONCAT: {
                StackValue b = pop_stack();
                StackValue a = pop_stack();
                
                if (a.type != TYPE_STRING || b.type != TYPE_STRING) {
                    fprintf(stderr, "Error: String concatenation requires two strings\n");
                    exit(1);
                }
                
                char result[MAX_STRING_SIZE];
                snprintf(result, sizeof(result), "%s%s", a.value.str_value, b.value.str_value);
                push_stack(make_string_value(result));
                
                free_stack_value(&a);
                free_stack_value(&b);
                break;
            }
            
            case OP_STR_LENGTH: {
                StackValue str = pop_stack();
                
                if (str.type != TYPE_STRING) {
                    fprintf(stderr, "Error: String length requires a string\n");
                    exit(1);
                }
                
                push_stack(make_int_value(strlen(str.value.str_value)));
                free_stack_value(&str);
                break;
            }
            
            case OP_STR_SLICE: {
                StackValue end_val = pop_stack();
                StackValue start_val = pop_stack();
                StackValue str = pop_stack();
                
                if (str.type != TYPE_STRING || start_val.type != TYPE_INT || end_val.type != TYPE_INT) {
                    fprintf(stderr, "Error: String slice requires a string and two integers\n");
                    exit(1);
                }
                
                int start = start_val.value.int_value;
                int end = end_val.value.int_value;
                int len = strlen(str.value.str_value);
                
                if (start < 0) start = 0;
                if (end > len) end = len;
                if (start >= len || end <= start) {
                    push_stack(make_string_value(""));
                } else {
                    char result[MAX_STRING_SIZE];
                    strncpy(result, str.value.str_value + start, end - start);
                    result[end - start] = '\0';
                    push_stack(make_string_value(result));
                }
                
                free_stack_value(&str);
                break;
            }
            
            case OP_STR_CONTAINS: {
                StackValue substr = pop_stack();
                StackValue str = pop_stack();
                
                if (str.type != TYPE_STRING || substr.type != TYPE_STRING) {
                    fprintf(stderr, "Error: String contains requires two strings\n");
                    exit(1);
                }
                
                push_stack(make_int_value(strstr(str.value.str_value, substr.value.str_value) != NULL ? 1 : 0));
                
                free_stack_value(&str);
                free_stack_value(&substr);
                break;
            }
            
            case OP_STR_SPLIT: {
                StackValue delim = pop_stack();
                StackValue str = pop_stack();
                
                if (str.type != TYPE_STRING || delim.type != TYPE_STRING) {
                    fprintf(stderr, "Error: String split requires two strings\n");
                    exit(1);
                }
                
                // Count number of tokens
                int count = 1;
                char *tmp = str.value.str_value;
                while ((tmp = strstr(tmp, delim.value.str_value)) != NULL) {
                    count++;
                    tmp += strlen(delim.value.str_value);
                }
                
                // Create array
                int array_id = array_count++;
                arrays[array_id].elements = malloc(count * sizeof(StackValue));
                arrays[array_id].size = count;
                
                // Split string
                char *copy = strdup(str.value.str_value);
                char *token = strtok(copy, delim.value.str_value);
                for (int i = 0; i < count && token != NULL; i++) {
                    arrays[array_id].elements[i] = make_string_value(token);
                    token = strtok(NULL, delim.value.str_value);
                }
                
                free(copy);
                push_stack(make_array_id_value(array_id));
                
                free_stack_value(&str);
                free_stack_value(&delim);
                break;
            }
            
            case OP_STR: {
                StackValue val = pop_stack();
                
                if (val.type == TYPE_INT) {
                    char result[MAX_STRING_SIZE];
                    snprintf(result, sizeof(result), "%d", val.value.int_value);
                    push_stack(make_string_value(result));
                } else if (val.type == TYPE_STRING) {
                    push_stack(val);  // Already a string
                } else {
                    fprintf(stderr, "Error: Cannot convert value to string\n");
                    exit(1);
                }
                break;
            }
            
            case OP_INPUT: {
                char input_buffer[MAX_STRING_SIZE];
                
                // Check if there's a prompt
                if (stack_size > 0 && stack[stack_size-1].type == TYPE_STRING) {
                    StackValue prompt = pop_stack();
                    printf("%s", prompt.value.str_value);
                    free_stack_value(&prompt);
                }
                
                if (fgets(input_buffer, sizeof(input_buffer), stdin) != NULL) {
                    // Remove trailing newline
                    size_t len = strlen(input_buffer);
                    if (len > 0 && input_buffer[len-1] == '\n') {
                        input_buffer[len-1] = '\0';
                    }
                    push_stack(make_string_value(input_buffer));
                } else {
                    push_stack(make_string_value(""));
                }
                break;
            }
            
            case OP_INPUT_INT: {
                char input_buffer[MAX_STRING_SIZE];
                
                // Check if there's a prompt
                if (stack_size > 0 && stack[stack_size-1].type == TYPE_STRING) {
                    StackValue prompt = pop_stack();
                    printf("%s", prompt.value.str_value);
                    free_stack_value(&prompt);
                }
                
                if (fgets(input_buffer, sizeof(input_buffer), stdin) != NULL) {
                    // Remove trailing newline
                    size_t len = strlen(input_buffer);
                    if (len > 0 && input_buffer[len-1] == '\n') {
                        input_buffer[len-1] = '\0';
                    }
                    
                    char *endptr;
                    long value = strtol(input_buffer, &endptr, 10);
                    
                    if (*endptr != '\0') {
                        fprintf(stderr, "Error: Input is not a valid integer\n");
                        exit(1);
                    }
                    
                    push_stack(make_int_value((int)value));
                } else {
                    fprintf(stderr, "Error: Failed to read input\n");
                    exit(1);
                }
                break;
            }
            
            case OP_FILE_OPEN: {
                StackValue mode = pop_stack();
                StackValue filename = pop_stack();
                
                if (mode.type != TYPE_STRING || filename.type != TYPE_STRING) {
                    fprintf(stderr, "Error: File open requires two strings\n");
                    exit(1);
                }
                
                // Find an empty file handle
                int handle = -1;
                for (int i = 0; i < MAX_FILES; i++) {
                    if (open_files[i] == NULL) {
                        handle = i;
                        break;
                    }
                }
                
                if (handle == -1) {
                    fprintf(stderr, "Error: Too many open files\n");
                    exit(1);
                }
                
                open_files[handle] = fopen(filename.value.str_value, mode.value.str_value);
                if (open_files[handle] == NULL) {
                    fprintf(stderr, "Error: Could not open file %s\n", filename.value.str_value);
                    exit(1);
                }
                
                push_stack(make_int_value(handle));
                
                free_stack_value(&mode);
                free_stack_value(&filename);
                break;
            }
            
            case OP_FILE_CLOSE: {
                StackValue handle_val = pop_stack();
                
                if (handle_val.type != TYPE_INT) {
                    fprintf(stderr, "Error: File close requires a file handle\n");
                    exit(1);
                }
                
                int handle = handle_val.value.int_value;
                if (handle < 0 || handle >= MAX_FILES || open_files[handle] == NULL) {
                    fprintf(stderr, "Error: Invalid file handle: %d\n", handle);
                    exit(1);
                }
                
                fclose(open_files[handle]);
                open_files[handle] = NULL;
                break;
            }
            
            case OP_FILE_READ: {
                StackValue handle_val = pop_stack();
                
                if (handle_val.type != TYPE_INT) {
                    fprintf(stderr, "Error: File read requires a file handle\n");
                    exit(1);
                }
                
                int handle = handle_val.value.int_value;
                if (handle < 0 || handle >= MAX_FILES || open_files[handle] == NULL) {
                    fprintf(stderr, "Error: Invalid file handle: %d\n", handle);
                    exit(1);
                }
                
                FILE *file = open_files[handle];
                char buffer[MAX_STRING_SIZE];
                size_t bytes_read = 0;
                
                // Get file size
                fseek(file, 0, SEEK_END);
                long file_size = ftell(file);
                fseek(file, 0, SEEK_SET);
                
                if (file_size >= MAX_STRING_SIZE - 1) {
                    fprintf(stderr, "Error: File too large to read\n");
                    exit(1);
                }
                
                bytes_read = fread(buffer, 1, file_size, file);
                buffer[bytes_read] = '\0';
                
                push_stack(make_string_value(buffer));
                break;
            }
            
            case OP_FILE_WRITE: {
                StackValue content = pop_stack();
                StackValue handle_val = pop_stack();
                
                if (handle_val.type != TYPE_INT) {
                    fprintf(stderr, "Error: File write requires a file handle\n");
                    exit(1);
                }
                
                int handle = handle_val.value.int_value;
                if (handle < 0 || handle >= MAX_FILES || open_files[handle] == NULL) {
                    fprintf(stderr, "Error: Invalid file handle: %d\n", handle);
                    exit(1);
                }
                
                FILE *file = open_files[handle];
                
                if (content.type == TYPE_STRING) {
                    fprintf(file, "%s", content.value.str_value);
                } else if (content.type == TYPE_INT) {
                    fprintf(file, "%d", content.value.int_value);
                } else {
                    fprintf(stderr, "Error: Cannot write unsupported type to file\n");
                    exit(1);
                }
                
                fflush(file);
                free_stack_value(&content);
                break;
            }
            
            case OP_FILE_APPEND: {
                StackValue content = pop_stack();
                StackValue handle_val = pop_stack();
                
                if (handle_val.type != TYPE_INT) {
                    fprintf(stderr, "Error: File append requires a file handle\n");
                    exit(1);
                }
                
                int handle = handle_val.value.int_value;
                if (handle < 0 || handle >= MAX_FILES || open_files[handle] == NULL) {
                    fprintf(stderr, "Error: Invalid file handle: %d\n", handle);
                    exit(1);
                }
                
                FILE *file = open_files[handle];
                
                if (content.type == TYPE_STRING) {
                    fprintf(file, "%s", content.value.str_value);
                } else if (content.type == TYPE_INT) {
                    fprintf(file, "%d", content.value.int_value);
                } else {
                    fprintf(stderr, "Error: Cannot append unsupported type to file\n");
                    exit(1);
                }
                
                fflush(file);
                free_stack_value(&content);
                break;
            }
            
            case OP_FUN_DEF: {
                // Function already registered in preprocess
                // Skip to matching FUN_END
                int nesting = 1;
                int temp_pc = pc + 1;
                
                while (temp_pc < program_size) {
                    if (program[temp_pc].code == OP_FUN_DEF) {
                        nesting++;
                    } else if (program[temp_pc].code == OP_FUN_END) {
                        nesting--;
                        if (nesting == 0) {
                            break;
                        }
                    }
                    temp_pc++;
                }
                
                if (temp_pc >= program_size) {
                    fprintf(stderr, "Error: Missing FUN_END for function '%s'\n", op.str_value);
                    exit(1);
                }
                
                pc = temp_pc;
                break;
            }
            
            case OP_FUN_END: {
                // Return from function
                if (call_stack_size > 0) {
                    pc = call_stack[--call_stack_size];
                }
                break;
            }
            
            case OP_FUN_CALL: {
                const char *fun_name = op.str_value;
                int fun_pos = -1;
                
                // Find function
                for (int i = 0; i < function_count; i++) {
                    if (strcmp(functions[i].name, fun_name) == 0) {
                        fun_pos = functions[i].position;
                        break;
                    }
                }
                
                if (fun_pos == -1) {
                    fprintf(stderr, "Error: Function '%s' not found\n", fun_name);
                    exit(1);
                }
                
                // Save return address
                if (call_stack_size >= sizeof(call_stack)/sizeof(call_stack[0])) {
                    fprintf(stderr, "Error: Call stack overflow\n");
                    exit(1);
                }
                
                call_stack[call_stack_size++] = pc;
                
                // Jump to function
                pc = fun_pos;
                continue;  // Skip pc increment
                break;
            }
            
            case OP_RETURN: {
                // Return from function
                if (call_stack_size > 0) {
                    pc = call_stack[--call_stack_size];
                } else {
                    fprintf(stderr, "Error: RETURN outside function\n");
                    exit(1);
                }
                break;
            }
            
            default:
                fprintf(stderr, "Error: Unknown operation code %d\n", op.code);
                exit(1);
        }
        
        pc++;
    }
    
    // Clean up
    for (int i = 0; i < array_count; i++) {
        if (arrays[i].elements != NULL) {
            for (int j = 0; j < arrays[i].size; j++) {
                free_stack_value(&arrays[i].elements[j]);
            }
            free(arrays[i].elements);
        }
    }
    
    for (int i = 0; i < var_count; i++) {
        free(var_names[i]);
        free_stack_value(&var_values[i]);
    }
    
    for (int i = 0; i < function_count; i++) {
        free(functions[i].name);
    }
    
    // Close any open files
    for (int i = 0; i < MAX_FILES; i++) {
        if (open_files[i] != NULL) {
            fclose(open_files[i]);
        }
    }
}

// Print a stack value
void print_stack_value(StackValue value) {
    switch (value.type) {
        case TYPE_INT:
            printf("%d\n", value.value.int_value);
            break;
        case TYPE_STRING:
            printf("%s\n", value.value.str_value);
            break;
        case TYPE_ARRAY_ID:
            printf("Array[%d]\n", value.value.array_id);
            break;
        default:
            printf("Unknown value type\n");
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
    
    // TODO: Generate assembly code for each operation
    
    // Data section for strings and other data
    fprintf(out, "section .data\n");
    fprintf(out, "fmt_int db \"%%d\", 10, 0\n");
    fprintf(out, "fmt_str db \"%%s\", 10, 0\n");
    
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
    
    // Initialize random seed
    srand(time(NULL));
    
    // Clean up globals before use
    program_size = 0;
    stack_size = 0;
    var_count = 0;
    function_count = 0;
    array_count = 0;
    
    parse_file(argv[2]);
    
    if (strcmp(argv[1], "sim") == 0) {
        int debug = (argc > 3 && strcmp(argv[3], "--debug") == 0);
        simulate_program(debug);
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
