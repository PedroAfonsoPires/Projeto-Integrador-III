import analisador_lexico as lex
import analisador_sintatico as sin
import geradorIntermediario as gi
import analisador_semantico as ase
import ParaMips as pmips  # Importa o módulo para converter para MIPS

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

# Converter código intermediário para MIPS
print("Convertendo o Código Intermediário para MIPS...")
mips_code = pmips.process_intermediate_to_mips(codI.split("\n"))
print("Código MIPS Gerado:")
print(mips_code)

# Salvar o código MIPS em um arquivo
output_file = "quick_sort.asm"
with open(output_file, 'w', encoding="utf-8") as f:
    f.write(mips_code)
print(f"Código MIPS salvo em {output_file}.")
