#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "Usage: ./valgrind.sh <executable>"
    exit 1
fi

executable=$1
valgrind --tool=memcheck --leak-check=full --track-origins=yes --error-exitcode=1 $executable
