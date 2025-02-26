#include <stdio.h>

int run_success = 0;

#define assert(x) if (x) {printf("Assert Passed!\n");} else {printf("Assertion failed: %s\n", #x);run_success = 1;}


int main(){
    assert(1);
    assert(0 == 3);
    assert(1 == 1);
    return run_success;
}
