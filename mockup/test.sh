#!/bin/bash
echo "Hello World!"

gcc -o test test.c >> output.txt 2>&1
./test >> output.txt 2>&1

# for i in {1..100000}
# do
# 	echo "Hello World!" >> output.txt
# done

