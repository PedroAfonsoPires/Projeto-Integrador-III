#include <stdio.h>

int main() {
    int num1, num2;
    char continuar;
    int maior, menor;
    float soma = 0.0;
    int contador = 0;

    do {
        // Entrada de dados
        printf("Digite dois números inteiros:\n");
        printf("Número 1: ");
        scanf("%d", &num1);
        printf("Número 2: ");
        scanf("%d", &num2);

        // Operações Bitwise
        printf("\nOperações Bitwise:\n");
        printf("AND bitwise (num1 & num2): %d\n", num1 & num2);
        printf("OR bitwise (num1 | num2): %d\n", num1 | num2);
        printf("XOR bitwise (num1 ^ num2): %d\n", num1 ^ num2);
        
        // Atualiza maior e menor
        if (contador == 0) {
            maior = menor = num1; // Inicializa maior e menor com o primeiro número
        } else {
            if (num1 > maior) maior = num1;
            if (num1 < menor) menor = num1;
        }
        
        if (num2 > maior) maior = num2;
        if (num2 < menor) menor = num2;

        // Soma e contador
        soma += num1 + num2;
        contador += 2;

        // Operações Lógicas
        printf("\nOperações Lógicas:\n");
        if (num1 > 0 && num2 > 0) {
            printf("Ambos os números são positivos.\n");
        } else if (num1 < 0 || num2 < 0) {
            printf("Pelo menos um dos números é negativo.\n");
        } else {
            printf("Ambos os números são zero ou negativos.\n");
        }

        // Pergunta se o usuário deseja continuar
        printf("\nDeseja continuar? (s/n): ");
        scanf(" %c", &continuar); // O espaço antes de %c ignora qualquer newline

    } while (continuar == 's' || continuar == 'S'); // Continua enquanto o usuário digitar 's' ou 'S'

    // Exibe resultados finais
    if (contador > 0) {
        float media = soma / contador;
        printf("\nResultados Finais:\n");
        printf("Maior número: %d\n", maior);
        printf("Menor número: %d\n", menor);
        printf("Média dos números: %.2f\n", media);
    } else {
        printf("Nenhum número foi digitado.\n");
    }

    printf("Programa encerrado.\n");

    // Laço de repetição adicional usando for
    printf("\nExibindo números de 1 a 10:\n");
    for (int i = 1; i <= 10; i++) {
        printf("%d ", i);
    }
    printf("\n");


    #include <stdio.h>

// Função para trocar os valores de duas variáveis usando ponteiros
void trocar(int *a, int *b) {
    int temp = *a;  // Armazena o valor de a
    *a = *b;        // Atribui o valor de b a a
    *b = temp;      // Atribui o valor de temp a b
}

// Função para calcular a soma de dois números usando ponteiros
void soma(int *num1, int *num2, int *resultado) {
    *resultado = *num1 + *num2;
}


    int x = 10, y = 20;
    int resultado;

    printf("Valores iniciais:\n");
    printf("x: %d, y: %d\n", x, y);

    // Exibindo endereços
    printf("\nEndereços de memória:\n");
    printf("&x: %p, &y: %p\n", (void*)&x, (void*)&y);

    // Usando a função trocar
    printf("\nTrocando valores de x e y...\n");
    trocar(&x, &y);
    printf("Valores após troca:\n");
    printf("x: %d, y: %d\n", x, y);

    // Usando a função soma
    soma(&x, &y, &resultado);
    printf("\nSoma de x e y: %d\n", resultado);
    return 0;
}
