import ply.lex as lex

# Lista de tokens
tokens = (
    'IF',
    'ELSE',
    'SWITCH',
    'WHILE',
    'FOR',
    'DO',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'POW',
    'LT',
    'GT',
    'LE',
    'GE',
    'EQ',
    'NE',
    'COMMENT',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COMMA',
    'LBRACK',
    'RBRACK',
    'STRING',
    'NUMBER',
    'AMPERSAND',
    'AND',
    'PIPE',
    'CHARACTER',
    'OR',
    'TYPEDEF',
    'DOT',
    'COLON',
    'HASH',
    'INT',
    'FLOAT',
    'CHAR',
    'DOUBLE',
    'VOID',
    'POINTER',
    'TYPE',
    'ID',
    'PLUS_PLUS',
    'MINUS_MINUS',
    'PLUS_EQUAL',
    'MINUS_EQUAL',
    'RETURN',
)

# Regras para tokens
t_COMMENT = r'//.*|/\*.*?\*/'
t_COLON = r':'
t_HASH = r'\#.*'
t_DOT = r'\.'
#t_IF = r'if'
#t_ELSE = r'else'
#t_SWITCH = r'switch'
#t_WHILE = r'while'
#t_FOR = r'for'
#t_DO_WHILE = r'do_while'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POW = r'\^'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_TYPEDEF = r'typedef'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'
t_NUMBER = r'\d+'
t_AMPERSAND = r'&'
t_AND = r'&&'
t_PIPE = r'\|'
t_OR = r'\|\|'
t_CHARACTER = r"'([^'\\]*(\\.[^'\\]*)*)'"
t_INT = r'int'
t_FLOAT = r'float'
t_VOID = r'void'
t_CHAR = r'char'
t_DOUBLE = r'double'
t_POINTER = r'\*'
t_TYPE = r'int|float|void|char|double'
t_PLUS_PLUS = r'\+\+'
t_MINUS_MINUS = r'--'
t_PLUS_EQUAL = r'\+='
t_MINUS_EQUAL = r'-='
#t_RETURN = r'return'
# Contador de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignorar espaços em branco e tabulações
t_ignore = r' \t'


# Regra para identificadores
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_RETURN(t):
    r'return'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_SWITCH(t):
    r'switch'
    return t

def t_FOR(t):
    r'for'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t


# Erros de caracteres ilegais
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Criar o analisador léxico
lexer = lex.lex()

# Função para processar o código de entrada
def process_code(data, k):
    lexer.input(data)
    if k != 0:
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(
                f"Token: {tok.type}, Valor: {tok.value}, Linha: {tok.lineno}")
