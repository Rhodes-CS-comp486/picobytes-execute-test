
    #include <stdio.h>
    #include <assert.h>

    #include <stdio.h>

int is_even(int n) {
return n % 2 == 0;
}
    int main(){
        assert(is_even(2) == 1);  // Passes
assert(is_even(3) == 1);
        return 0;
    }
    