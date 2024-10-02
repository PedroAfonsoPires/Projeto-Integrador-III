import ply.lex as lex

#Lista de tokens
tokens = (
    'IF', 'ELSE', 'SWITCH', 'WHILE', 'FOR', 'DO_WHILE', 'ASSIGN',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'POW', 'LT', 'GT',
    'LE', 'GE', 'EQ', 'NE', 'COMMENT', 'ID', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE', 'INCLUDE', 'SEMICOLON', 'COMMA', 'LBRACK', 'RBRACK',
    'STRING', 'NUMBER', 'FLOAT', 'AMPERSAND',
)


#Regra para diretivas de pré-processamento
t_INCLUDE = r'\#\s*include\s*<([a-zA-Z0-9_.]+)>'

#Regras para tokens de comandos condicionais
t_IF     = r'if'
t_ELSE   = r'else'
t_SWITCH = r'switch'

#Regras para tokens de comandos de laço
t_WHILE    = r'while'
t_FOR      = r'for'
t_DO_WHILE = r'do_while'

#Regra para operador de atribuição
t_ASSIGN = r'='

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MOD    = r'%'
t_POW    = r'\^'

#Regras para operadores de comparação
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

#Regra para comentários (de linha e bloco)
t_COMMENT = r'//.*|/\*.*?\*/'

#Regra para identificadores
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

#Regras para parênteses e chaves
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

#Regras para colchetes
t_LBRACK = r'\['
t_RBRACK = r'\]'

#Regra para vírgula
t_COMMA = r','

#Regra para ponto e vírgula
t_SEMICOLON = r';'

#Regra para strings
t_STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'

#Regra para números inteiros
t_NUMBER = r'\d+'

#Regra para números reais
t_FLOAT = r'\d+\.\d+'

#Ignorar espaços em branco
t_ignore = r' \t'

# Regra para o operador '&'
t_AMPERSAND = r'&'

#Contador de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Erros de caracteres ilegais
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

#Tabela de símbolos
symbol_table = {}

#Criar o analisador léxico
lexer = lex.lex()

#Função para processar o código de entrada
def process_code(data):
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        #Adiciona à tabela de símbolos
        if tok.type not in symbol_table:
            symbol_table[tok.type] = []
        symbol_table[tok.type].append((tok.value, tok.lineno))
        print(f"Token: {tok.type}, Valor: {tok.value}, Linha: {tok.lineno}")

#Código de exemplo em C
name = input();
with open(name, 'r', encoding="utf-8") as file_:
    c_code = file_.read();

#Processar o código de entrada
process_code(c_code)

#Exibir a tabela de símbolos
print("\nTabela de Símbolos:")
for token_type, occurrences in symbol_table.items():
    print(f"{token_type}: {occurrences}")