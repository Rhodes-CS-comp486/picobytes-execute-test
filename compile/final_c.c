
    int run_success = 0;
    #define assert(condition) if (condition) {printf("ASSERT PASSED!\n");} else {printf("ASSERT FAILED: %s\n", #condition);run_success = 1;}
        
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
return result;
}

        int main(){
            assert(factorial(3) == 6);
assert(factorial(4) == 120);
assert(factorial(0) == 1);
assert(factorial(-1) == 0);
            return run_success;
        }
            