#include <stdio.h>
#include <string.h>

// Definindo um enum para o status do estudante
enum StatusEstudante {
    MATRICULADO,
    CANCELADO,
    FORMADO
};

// Definindo uma struct para representar um estudante sem typedef
struct EstudanteSemTypedef {
    char nome[50];
    int idade;
    enum StatusEstudante status;
};

// Definindo uma struct para representar um estudante com typedef
typedef struct {
    char nome[50];
    int idade;
    enum StatusEstudante status;
} EstudanteComTypedef;

// Função para exibir informações do estudante sem typedef
void exibirEstudanteSemTypedef(struct EstudanteSemTypedef e) {
    printf("Nome: %s\n", e.nome);
    printf("Idade: %d\n", e.idade);
    printf("Status: ");
    switch (e.status) {
        case MATRICULADO: printf("MATRICULADO\n"); break;
        case CANCELADO: printf("CANCELADO\n"); break;
        case FORMADO: printf("FORMADO\n"); break;
    }
}

// Função para exibir informações do estudante com typedef
void exibirEstudanteComTypedef(EstudanteComTypedef e) {
    printf("Nome: %s\n", e.nome);
    printf("Idade: %d\n", e.idade);
    printf("Status: ");
    switch (e.status) {
        case MATRICULADO: printf("MATRICULADO\n"); break;
        case CANCELADO: printf("CANCELADO\n"); break;
        case FORMADO: printf("FORMADO\n"); break;
    }
}

int main() {
    // Criando e inicializando um estudante sem typedef
    struct EstudanteSemTypedef estudante1;
    strcpy(estudante1.nome, "Maria Silva");
    estudante1.idade = 20;
    estudante1.status = MATRICULADO;

    // Exibindo informações do estudante sem typedef
    printf("Informações do Estudante (sem typedef):\n");
    exibirEstudanteSemTypedef(estudante1);

    // Criando e inicializando um estudante com typedef
    EstudanteComTypedef estudante2;
    strcpy(estudante2.nome, "João Souza");
    estudante2.idade = 22;
    estudante2.status = FORMADO;

    // Exibindo informações do estudante com typedef
    printf("\nInformações do Estudante (com typedef):\n");
    exibirEstudanteComTypedef(estudante2);

    return 0;
}
