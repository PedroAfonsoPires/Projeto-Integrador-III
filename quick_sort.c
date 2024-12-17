#include <stdio.h>

int main() {
    int x = 10;
    int y = 20;

    // Declaração com atribuição
    float z = 0;
    float w[10]; // Vetor com tamanho 10

    // If statement
    if (x < y) {
        z = x + y;
    }

    // If-else statement
    if (z > 30) {
        printf("z is greater than 30\n");
    } else {
        printf("z is less than or equal to 30\n");
    }

    // While loop
    int counter = 0;
    while (counter < 5) {
        printf("Counter: %d\n", counter);
        counter++;
    }

    // Do-while loop
    int count_down = 5;
    do {
        printf("Counting down: %d\n", count_down);
        count_down--;
    } while (count_down > 0);

    // For loop
    for (int i = 0; i < 5; i++) {
        printf("For loop iteration: %d\n", i);
    }

    return 0;
}