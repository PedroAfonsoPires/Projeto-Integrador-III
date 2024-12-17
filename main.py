import analisador_lexico as lex
import analisador_sintatico as sin
import analisador_semantico as sem  # Importa o analisador semântico

# Código de exemplo em C (para ser processado pelo analisador léxico e sintático)
name = "quick_sort1.c"
with open(name, 'r', encoding="utf-8") as file_:
    c_code = file_.read()

# Processar o código de entrada com o analisador léxico
print("Processando o código com o analisador léxico...")
lex.process_code(c_code, 0)

# Executar o analisador sintático
print("Analisando o código com o analisador sintático...")
ast = sin.parse_code(c_code, 0)
print("Análise Sintática concluída.")
print("AST gerada:")
print(ast)

# Executar o analisador semântico
print("Executando o analisador semântico...")
semantic_analyzer = sem.SemanticAnalyzer()  # Inicializa o analisador semântico
try:
    semantic_analyzer.analyze(ast)  # Realiza a análise semântica na AST
    print("Análise Semântica concluída sem erros.")
except RuntimeError as e:
    print(f"Erro na análise semântica: {e}")

# Gerar código intermediário
print("Gerador do Código Intermediário...")
codI = semantic_analyzer.analyze(ast)
print("Código Intermediário Gerado:")
print(codI)
print("Geração concluída.")