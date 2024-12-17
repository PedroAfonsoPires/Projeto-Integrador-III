import analisador_lexico as lex
import analisador_sintatico as sin
import geradorIntermediario as gi

# Código de exemplo em C (para ser processado pelo analisador léxico e sintático)
name = "quick_sort.c"
with open(name, 'r', encoding="utf-8") as file_:
    c_code = file_.read()

# Processar o código de entrada com o analisador léxico
print("Processando o código com o analisador léxico...")
lex.process_code(c_code, 0)

# Executar o analisador sintático
print("Analisando o código com o analisador sintático...")
ast = sin.parse_code(c_code, 0)
print("Análise concluída.")



# Gerar código intermediário
print("Gerador do Código Intermediário...")
codI = gi.process_node(ast)
print("Código Intermediário Gerado:")
print(codI)
print("Geração concluída.")
