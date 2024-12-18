#include <stdio.h>

// Função para trocar dois elementos
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Particiona o array e retorna o índice do pivô
int partition(int arr[], int low, int high) {
    int pivot = arr[high]; // Escolhe o último elemento como pivô
    int i = (low - 1); // Índice do menor elemento

    for (int j = low; j < high; j++) {
        // Se o elemento atual é menor ou igual ao pivô
        if (arr[j] <= pivot) {
            i++; // Incrementa o índice do menor elemento
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]); // Coloca o pivô na posição correta
    return (i + 1);
}

// Função principal do Quicksort
void quicksort(int arr[], int low, int high) {
    if (low < high) {
        // Particiona o array e obtém o índice do pivô
        int pi = partition(arr, low, high);

        // Ordena recursivamente as duas metades
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

// Função para imprimir o array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Função principal
int main() {
    int arr[] = {10, 7, 8, 9, 1, 5};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array original: ");
    printArray(arr, n);

    quicksort(arr, 0, n - 1);

    printf("Array ordenado: ");
    printArray(arr, n);
    return 0;
}
