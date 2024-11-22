import ply.yacc as yacc
from analisador_lexico import tokens
import sys

def parse_code(data):
    parser = yacc.yacc(debug=True, debuglog=yacc.PlyLogger(sys.stderr))
    result = parser.parse(data)
    print("Árvore Sintática:")
    print(result)
    return result



def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]


def p_comment(p):
    '''statement : COMMENT'''
    pass


def p_preprocessor_directive(p):
    '''statement : HASH'''
    pass


def p_statement(p):
    '''statement : declaration
                 | declaration_func
                 | expression_statement
                 | if_expression
                 | for_expreression
                 | while_expression
                 | while_do_expression
                 | return'''
    p[0] = p[1]


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_declaration(p): #arrumar vetor
    '''declaration : TYPE ID SEMICOLON
                   | TYPE ID ASSIGN expression SEMICOLON
                   | TYPE ID ASSIGN funct
                   | TYPE ID ASSIGN block
                   | TYPE TIMES ID
                   | TYPE vector
                   | TYPE vector SEMICOLON
                   | TYPE TIMES vector SEMICOLON
                   | TYPE ID LBRACK RBRACK
                   | TYPE ID LBRACK RBRACK ASSIGN expression SEMICOLON'''

    if len(p) == 4: #caso type a;
        p[0] = ('declaration', p[1], p[2])
    elif len(p) == 5: # caso type *a;
        p[0] = ('declaration', p[1], 'pointer', p[3])
    elif len(p) == 6: # type a = expression
        p[0] = ('declaration', p[1], p[2], p[4])
    else:
        p[0] = p[1]


def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON
                            | expression'''
    p[0] = ('expr_stmt', p[1])


def p_expression(p): #arrumar saida para pontei
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | ID
                  | NUMBER
                  | TIMES ID
                  | expression ASSIGN expression
                  | STRING
                  | LPAREN expression RPAREN
                  | vector
                  | expression PLUS_PLUS
                  | expression MINUS_MINUS
                  | expression PLUS_EQUAL
                  | expression MINUS_EQUAL
                  | block
                  | expression COMMA expression
                  | funct'''

    if len(p) == 4:
        p[0] =  (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_parameters(p):
    '''parameters : TYPE ID
                  | TYPE ID COMMA parameters
                  | TYPE TIMES ID
                  | TYPE TIMES ID COMMA parameters
                  | TYPE ID LBRACK RBRACK
                  | TYPE ID LBRACK RBRACK COMMA parameters
                  | TYPE vector COMMA parameters
                  | ID COMMA parameters
                  | TIMES ID
                  | TIMES ID COMMA parameters
                  | ID LBRACK RBRACK
                  | ID LBRACK RBRACK COMMA parameters
                  | vector COMMA parameters
                  | expression
                  | parameters COMMA parameters'''

    if len(p) == 3:
        p[0] = ('parameter', p[1], p[2])  # Caso para TYPE ID
    elif len(p) == 4:
        p[0] = ('parameter', p[1], f"*{p[2]}")  # Caso para TYPE TIMES ID
    elif len(p) == 6:
        p[0] = ('parameter', p[1], p[2])  # Caso para TYPE ID COMMA parameters
    elif len(p) == 7:
        p[0] = ('parameter', p[1], f"*{p[2]}")  # Caso para TYPE TIMES ID COMMA parameters


def p_declaration_func(p): #arrunar a saida
    '''declaration_func : TYPE ID LPAREN parameters RPAREN block
                        | TYPE ID LPAREN RPAREN block'''
    p[0] = ('function_declaration', p[1], p[2], p[4], p[5])

def p_funct(p):
    '''funct : ID LPAREN parameters RPAREN
             | ID LPAREN RPAREN'''

def p_if_expression(p): #arrumar saida
    '''if_expression : IF LPAREN condicional RPAREN block
                     | IF LPAREN condicional RPAREN block ELSE block'''

def p_condicional(p): #ARRUMAR SAIDA
    '''condicional : ID operadoror_comp ID
                   | ID operadoror_comp NUMBER
                   | ID operadoror_comp vector
                   | NUMBER operadoror_comp ID
                   | NUMBER operadoror_comp NUMBER
                   | NUMBER operadoror_comp vector
                   | vector operadoror_comp ID
                   | vector operadoror_comp NUMBER
                   | vector operadoror_comp vector'''

def p_vector(p):
    '''vector : ID LBRACK expression RBRACK
              | AMPERSAND vector'''

def p_block(p):
    '''block : LBRACE statement_list RBRACE
             | LBRACE RBRACE'''

    p[0] = ('block', p[2])

def p_operador_comp(p):
      '''operadoror_comp : EQ
                   | NE
                   | GE
                   | LE
                   | GT
                   | LT'''

def p_for_expression(p): #ARRUMAR saida
    '''for_expreression : FOR LPAREN declaration ID operadoror_comp ID SEMICOLON ID PLUS_PLUS RPAREN block
                        | FOR LPAREN declaration ID operadoror_comp ID SEMICOLON ID MINUS_MINUS RPAREN block
                        | FOR LPAREN declaration ID operadoror_comp NUMBER SEMICOLON ID PLUS_PLUS RPAREN block
                        | FOR LPAREN declaration ID operadoror_comp NUMBER SEMICOLON ID MINUS_MINUS RPAREN block'''

def p_while_expression(p):
    '''while_expression : WHILE LPAREN ID operadoror_comp ID RPAREN block
                        | WHILE LPAREN ID operadoror_comp NUMBER RPAREN block
                        | WHILE LPAREN NUMBER operadoror_comp ID RPAREN block
                        | WHILE LPAREN NUMBER operadoror_comp NUMBER RPAREN block'''

def p_while_do_expression(p):
    '''while_do_expression : DO block WHILE LPAREN ID operadoror_comp ID RPAREN SEMICOLON
                           | DO block WHILE LPAREN ID operadoror_comp NUMBER RPAREN SEMICOLON
                           | DO block WHILE LPAREN NUMBER operadoror_comp ID RPAREN SEMICOLON
                           | DO block WHILE LPAREN NUMBER operadoror_comp NUMBER RPAREN SEMICOLON'''

def p_return(p):
    ''' return : RETURN expression SEMICOLON'''

def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: {p.value}")
    else:
        print("Erro de sintaxe: final inesperado.")
