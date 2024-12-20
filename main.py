import analisador_lexico as lex
import analisador_sintatico as sin
import analisador_semantico as sem
import geradorIntermediario as gi
import ParaMips as pmips
import sys
# Código de exemplo em C (para ser processado pelo analisador léxico e sintático)
name = sys.argv[1]
with open(name, 'r', encoding="utf-8") as file_:
    c_code = file_.read()

# Processar o código de entrada com o analisador léxico
print("Processando o código com o analisador léxico...")
lex.process_code(c_code, 1)

print()

# Executar o analisador sintático
print("Analisando o código com o analisador sintático...")
ast = sin.parse_code(c_code, 0)
print("Análise Sintática concluída.")

print()

# Executar o analisador semântico
print("Executando o analisador semântico...")
semantic_analyzer = sem.SemanticAnalyzer()  # Inicializa o analisador semântico
try:
    semantic_analyzer.analyze(ast)  # Realiza a análise semântica na AST
    print("Análise Semântica concluída sem erros.")
except RuntimeError as e:
    print(f"Erro na análise semântica: {e}")

symbol_table = semantic_analyzer.get_all_symbols()
sem.show_symbol_table(symbol_table)

print()

# Gerar código intermediário
print("Gerador do Código Intermediário...")
codI = gi.process_node(ast, symbol_table)
print("Código Intermediário Gerado:")
print(codI)
print("Geração concluída.")

print()


# Converter código intermediário para MIPS
print("Convertendo o Código Intermediário para MIPS...")
mips_code = pmips.process_intermediate_to_mips(codI.split("\n"))
print("Código MIPS Gerado:")
print(mips_code)

# Salvar o código MIPS em um arquivo
output_file = name + ".asm"
with open(output_file, 'w', encoding="utf-8") as f:
    f.write(mips_code)
print(f"Código MIPS salvo em {output_file}.")
