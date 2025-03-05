
#!/bin/bash

# Script to compile a Backstack program to an executable
# Usage: ./compile_bs.sh <input_file.bs> [output_name]

set -e  # Exit on error

if [ $# -lt 1 ]; then
    echo "Usage: $0 <input_file.bs> [output_name]"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_NAME="${2:-$(basename "${INPUT_FILE%.*}")}"
ASM_FILE="${OUTPUT_NAME}.asm"
OBJ_FILE="${OUTPUT_NAME}.o"
EXE_FILE="${OUTPUT_NAME}"

# Check if we're on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    EXE_FILE="${OUTPUT_NAME}.exe"
    ASM_FORMAT="win64"
    LINK_ARGS="-o ${EXE_FILE}"
else
    ASM_FORMAT="elf64"
    LINK_ARGS="-no-pie -o ${EXE_FILE}"
fi

echo "Compiling ${INPUT_FILE} to assembly..."
python src/python/main.py com "${INPUT_FILE}" "${ASM_FILE}"

echo "Assembling with NASM..."
nasm -f ${ASM_FORMAT} "${ASM_FILE}" -o "${OBJ_FILE}"

echo "Linking with GCC..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    gcc "${OBJ_FILE}" ${LINK_ARGS} -nostdlib -lkernel32 -lmsvcrt
else
    gcc "${OBJ_FILE}" ${LINK_ARGS}
fi

echo "Compilation successful: ${EXE_FILE}"
echo "Run with: ./${EXE_FILE}"
