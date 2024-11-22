#include <stdio.h>

// Função para trocar dois elementos
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}
