#include <assert.h>
    #include <stdio.h>
    #include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main2() {
int randomNumber, guess, attempts = 0;

while (1){}
// Seed random number generator
srand(time(0));
randomNumber = rand() % 100 + 1; // Random number between 1 and 100

printf("Welcome to the Number Guessing Game!\n");
printf("Try to guess the number between 1 and 100.\n");

// Game loop
do {
printf("Enter your guess: ");
scanf("%d", &guess);
attempts++;

if (guess > randomNumber) {
printf("Too high! Try again.\n");
} else if (guess < randomNumber) {
printf("Too low! Try again.\n");
} else {
printf("Congratulations! You guessed the number in %d attempts.\n", attempts);
}
} while (guess != randomNumber);

return 0;
}
    int main(){
    assert(main2() == 0);
    return 0;
    }