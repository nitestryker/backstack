
# Makefile for building Backstack compiler

CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = backstack.exe

all: $(TARGET)

$(TARGET): backstack.c
	$(CC) $(CFLAGS) -o $(TARGET) backstack.c

clean:
	rm -f $(TARGET) output.asm output.o

.PHONY: all clean
