from symbol_table import SymbolTable

def show_symbol_table(symbol_table):
    """Exibe os símbolos em todos os escopos da tabela de símbolos."""
    print("\n--- Tabela de Símbolos ---")
    for i, scope in enumerate(reversed(symbol_table.current_scope)):
        print(f"Escopo {len(symbol_table.current_scope) - i - 1}:")
        if scope:
            for name, attributes in scope.items():
                print(f"  Name: {name}, Attributes: {attributes}")
        else:
            print("  [Vazio]")
    print("--------------------------")

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.report = {
            "symbols": [],
            "errors": []
        }

    def analyze(self, ast):
        """Percorre a AST e aplica regras semânticas."""
        try:
            for node in ast:
                self.visit(node)
        except RuntimeError as e:
            self.report["errors"].append(str(e))

    def visit(self, node):
        """Método genérico para visitar nós da AST."""
        print(f"Visiting node: {node}")  # Log de debug
        method_name = f"visit_{node[0]}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print(f"Warning: Nenhum visitador definido para o nó: {node[0]}")
        return None

    def visit_preprocessor_directive(self, node):
        """Visita uma diretiva de pré-processador e a ignora."""
        print(f"Ignorando diretiva de pré-processador: {node[1]}")

    def visit_declaration(self, node):
        """Visita uma declaração de variável."""
        _, var_type, var_name = node[:3]
        value = None

        # Verifica se há um valor de inicialização
        if len(node) == 4:  # Inicialização
            value = node[3]
            # Verifica se o tipo de variável é compatível com o valor
            if not self.check_type_compatibility(var_type, value):
                raise RuntimeError(f"Incompatibilidade de tipos ao inicializar '{var_name}'.")

        # Adiciona o símbolo à tabela
        self.symbol_table.add_symbol(var_name, {"type": var_type, "value": value})
        self.report["symbols"].append({"name": var_name, "type": var_type, "value": value})
        return {"name": var_name, "type": var_type, "value": value}

    def visit_literal(self, node):
        """Visita um valor literal e retorna seu tipo."""
        value = node  # Agora trata diretamente o valor (node é o valor literal)
        if isinstance(value, str) and value.isdigit():
            return int(value)  # Converte strings numéricas para inteiros
        return value  # Retorna o valor se não for um número


    def check_type_compatibility(self, type1, type2):
        """Verifica a compatibilidade de tipos."""
        if type1 is None or type2 is None:
            raise RuntimeError("Erro de compatibilidade: um dos tipos é None.")

        # Tenta converter o tipo2 (valor) se for uma string representando um número
        if isinstance(type2, str):
            # Se for uma string representando um número inteiro
            if type2.isdigit():
                type2 = int(type2)
            # Se for uma string representando um número de ponto flutuante
            elif type2.replace('.', '', 1).isdigit() and type2.count('.') < 2:
                type2 = float(type2)

        # Verifica a compatibilidade de tipos
        if isinstance(type2, int) and type1 == "int":
            return True
        elif isinstance(type2, float) and type1 == "float":
            return True
        elif isinstance(type2, str) and type1 == "str":
            return True
        return False


    def generate_report(self):
        """Gera um relatório com informações coletadas durante a análise."""
        print("--- Relatório de Análise Semântica ---")
        print("Símbolos declarados:")
        for symbol in self.report["symbols"]:
            print(f"- {symbol}")
        print("\nErros encontrados:")
        for error in self.report["errors"]:
            print(f"- {error}")
        print("------------------------------------")

    def get_all_symbols(self):
        return self.symbol_table

    def visit_function_declaration(self, node):
        """Visita uma declaração de função."""
        _, return_type, name, block = node  # Extrai os elementos do nó da função
        print(f"Visiting function declaration: {name} with return type {return_type}")

        # Adiciona a função à tabela de símbolos no escopo global
        self.symbol_table.add_symbol(name, {"type": f"function ({return_type})", "params": []})

        # Entra no escopo da função
        self.symbol_table.enter_scope()

        # Processa cada instrução no bloco da função
        for stmt in block[1]:  # Considera que o bloco é uma lista de declarações ou instruções
            self.visit(stmt)

        # Sai do escopo da função
        self.symbol_table.exit_scope()

    def visit_expr_stmt(self, node):
        """Visita uma instrução de expressão (por exemplo, atribuição ou operação)."""
        # No caso de uma atribuição, o nó será algo como ('=', 'z', ('+', 'x', 'y'))
        op = node[0]  # Operador (por exemplo, '=' para atribuição)

        if op != '=':
            raise RuntimeError(f"Operação desconhecida: {op}")

        if len(node) < 3:
            raise RuntimeError(f"Erro: nó de expressão de atribuição mal formado: {node}")

        left = node[1]  # Lado esquerdo da atribuição (por exemplo, 'z')
        right = node[2]  # Lado direito da atribuição (por exemplo, ('+', 'x', 'y'))

        # Verifique se a variável à esquerda existe na tabela de símbolos
        if left not in self.symbol_table.get_symbol(left):
            raise RuntimeError(f"Erro: '{left}' não declarado.")

        # Aqui você pode verificar a compatibilidade de tipos entre o lado esquerdo e o lado direito
        right_value = self.visit(right)  # Avalia a expressão do lado direito
        left_type = self.symbol_table.get_symbol(left)['type']  # Tipo da variável à esquerda

        if not self.check_type_compatibility(left_type, right_value):
            raise RuntimeError(f"Incompatibilidade de tipos: '{left}' não pode receber um valor do tipo {type(right_value)}.")

        # Se a variável à esquerda não foi declarada, adicione à tabela de símbolos
        self.symbol_table.add_symbol(left, {"type": left_type, "value": right_value})

    def visit_return(self, node):
        """Visita uma expressão de retorno."""
        # O nó de return deve ser algo como ('return', expressão)
        if len(node) == 2:
            return_expr = node[1]  # Expressão após o 'return'
            return_value = return_expr  # Avalia a expressão do retorno #arrumar
            print(f"Retornando o valor: {return_value}")
            return return_value

    def visit_comment(self, node):
        """Visita um comentário e o ignora."""
        print(f"Ignorando comentário: {node[1]}")

