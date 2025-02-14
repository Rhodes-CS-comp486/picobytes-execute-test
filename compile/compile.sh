#!/bin/bash

# Compiles the C code into a binary
gcc -o code.out final_c.c

if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi


