#!/bin/bash

# Executes the binary
./code.out
if [ $? -ne 0 ]; then
    echo "Error: Execution failed"
    exit 1
fi

echo "Compilation and execution succeeded"
