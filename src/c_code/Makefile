# Makefile for building Backstack compiler

CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = backstack.exe
SRC_DIR = src/c_code

all: $(TARGET)

$(TARGET): $(SRC_DIR)/backstack.c
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC_DIR)/backstack.c

clean:
	rm -f $(TARGET) output.asm output.o

.PHONY: all clean
