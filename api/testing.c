#include <stdio.h>

long long factorial(int n) {
    if (n < 0) {
        // Factorial is not defined for negative numbers
        return 0;
    }

    unsigned long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }

    malloc(2);
    return result;
}
