#include <stdio.h>

int main() {
    int opcao;
    float num1, num2, resultado;

    printf("Calculadora Simples\n");
    printf("Selecione uma operação:\n");
    printf("1. Adição\n");
    printf("2. Subtração\n");
    printf("3. Multiplicação\n");
    printf("4. Divisão\n");
    printf("Digite sua opção (1-4): ");
    scanf("%d", &opcao);

    // Verifica se a opção está dentro do intervalo válido
    if (opcao < 1 || opcao > 4) {
        printf("Opção inválida! Por favor, escolha uma opção entre 1 e 4.\n");
        return 1; // Encerra o programa com erro
    }

    // Solicita os números ao usuário
    printf("Digite o primeiro número: ");
    scanf("%f", &num1);
    printf("Digite o segundo número: ");
    scanf("%f", &num2);

    // Realiza a operação com base na opção escolhida
    switch (opcao) {
        case 1:
            resultado = num1 + num2;
            printf("Resultado da Adição: %.2f\n", resultado);
            break;
        case 2:
            resultado = num1 - num2;
            printf("Resultado da Subtração: %.2f\n", resultado);
            break;
        case 3:
            resultado = num1 * num2;
            printf("Resultado da Multiplicação: %.2f\n", resultado);
            break;
        case 4:
            if (num2 != 0) {
                resultado = num1 / num2;
                printf("Resultado da Divisão: %.2f\n", resultado);
            } else {
                printf("Erro: Divisão por zero não é permitida!\n");
            }
            break;
        default:
            printf("Opção inválida!\n");
            break;
    }

    return 0;
}
