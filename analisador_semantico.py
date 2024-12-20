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
        for node in ast:
            try:
                self.visit(node)
            except RuntimeError as e:
                self.report["errors"].append(str(e))

    def visit(self, node):
        """Método genérico para visitar nós da AST."""
        print(f"Visiting node: {node}")  # Log de debug

        # Se o nó for um operador de comparação
        if node[0] in ('<', '>', '==', '!=', '<=', '>='):
            return self.visit_comparison_operator(node)

        # Se o nó é uma string, pode ser um identificador (nome de variável)
        if isinstance(node, str):  # Se o nó for uma string (nome de variável)
            return self.symbol_table.get_symbol(node)["value"]

        method_name = f"visit_{node[0]}"  # Ex: visit_declaration, visit_if, etc.
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        print(f"Warning: Nenhum visitador definido para o nó: {node[0]}")
        return None

    def visit_preprocessor_directive(self, node):
        """Visita uma diretiva de pré-processador e a ignora."""
        print(f"Ignorando diretiva de pré-processador: {node[1]}")

    def visit_declaration(self, node):
        """Visita uma declaração de variável, incluindo vetores e ponteiros."""
        _, var_type, var_name = node[:3]
        value = None

        # Verifica se o tipo é um vetor (ou qualquer outra estrutura especial)
        if isinstance(var_name, tuple) and var_name[0] == 'vector':
            vector_name = var_name[1]
            # Aqui você pode adicionar a lógica específica para vetores
            self.symbol_table.add_symbol(vector_name, {"type": f"vector({var_type})", "value": None})
            self.report["symbols"].append({"name": vector_name, "type": f"vector({var_type})", "value": None})
            return {"name": vector_name, "type": f"vector({var_type})", "value": None}

        # Caso normal: variável simples
        if len(node) == 4:  # Se houver valor de inicialização
            try:
                value = self.visit(node[3])
            except:
                value = node[3]
            # Verifica a compatibilidade de tipo
            if not self.check_type_compatibility(var_type, value):
                raise RuntimeError(f"Incompatibilidade de tipos ao inicializar '{var_name}'.")

        # Adiciona o símbolo à tabela de símbolos
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
        _, return_type, name, *params_and_block = node  # Ajusta para lidar com mais elementos
        params = []
        block = None

        # Separa os parâmetros e o bloco de código
        for item in params_and_block:
            if item[0] == 'parameter':
                params.append(item)
            elif item[0] == 'block':
                block = item

        print(f"Visiting function declaration: {name} with return type {return_type}")
        print(f"Parameters: {params}")

        # Adiciona a função à tabela de símbolos no escopo global
        self.symbol_table.add_symbol(name, {"type": f"function ({return_type})", "params": params})

        # Entra no escopo da função
        self.symbol_table.enter_scope()

        # Processa cada instrução no bloco da função
        if block:
            for stmt in block[1]:  # Considera que o bloco contém uma lista de declarações ou instruções
                self.visit(stmt)

        # Sai do escopo da função
        self.symbol_table.exit_scope()


    def visit_expr_stmt(self, node):
        """Visita uma instrução de expressão (por exemplo, atribuição ou operação)."""
        op = node[0]  # Operador (por exemplo, '=' para atribuição)

        if op != '=':
            raise RuntimeError(f"Operação desconhecida: {op}")

        if len(node) < 3:
            raise RuntimeError(f"Erro: nó de expressão de atribuição mal formado: {node}")

        left = node[1]  # Lado esquerdo da atribuição
        right = node[2]  # Lado direito da atribuição

        # Verifique se a variável à esquerda existe na tabela de símbolos
        if left not in self.symbol_table.get_symbol(left):
            raise RuntimeError(f"Erro: '{left}' não declarado.")

        # Verifique se o lado direito é uma desreferenciação (por exemplo, ('a', '*'))
        if isinstance(right, tuple) and right[1] == "*":
            # Aqui, o lado direito é uma desreferenciação, então verifique se 'a' é um ponteiro
            pointer_var = right[0]
            pointer_type = self.symbol_table.get_symbol(pointer_var)["type"]
            if not pointer_type.startswith("pointer"):
                raise RuntimeError(f"Erro: '{pointer_var}' não é um ponteiro e não pode ser desreferenciado.")

            # O tipo à esquerda deve ser compatível com o tipo apontado
            pointer_base_type = pointer_type[len("pointer("):-1]  # Tipo apontado
            left_type = self.symbol_table.get_symbol(left)["type"]
            if left_type != pointer_base_type:
                raise RuntimeError(f"Incompatibilidade de tipos: '{left}' não pode receber um valor do tipo {left_type}.")

        else:
            # Caso normal (sem desreferenciação)
            right_value = self.visit(right)  # Avalia a expressão do lado direito
            left_type = self.symbol_table.get_symbol(left)["type"]  # Tipo da variável à esquerda

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

    def visit_if(self, node):
        """Visita uma instrução 'if'."""
        # Ajuste para suportar a ausência do bloco "else"
        _, condition, then_block, *else_block = node
        else_block = else_block[0] if else_block else None

        print(f"Visiting 'if' statement with condition: {condition}")

        # Avaliar a expressão condicional
        condition_value = self.visit(condition)

        # Verifica se o tipo da condição é booleano ou compatível
        if not isinstance(condition_value, bool):
            raise RuntimeError(f"Erro de tipo: a condição de 'if' deve ser um valor booleano, mas recebeu {type(condition_value)}.")

        # Processa o bloco "then"
        print("Entering 'then' block:")
        self.symbol_table.enter_scope()
        for stmt in then_block[1]:  # Assumindo que o bloco contém uma lista de declarações ou instruções
            self.visit(stmt)
        self.symbol_table.exit_scope()

        # Processa o bloco "else", se houver
        if else_block:
            print("Entering 'else' block:")
            self.symbol_table.enter_scope()
            for stmt in else_block[1]:  # Assumindo que o bloco contém uma lista de declarações ou instruções
                self.visit(stmt)
            self.symbol_table.exit_scope()


    def visit_while(self, node):
        """Visita uma instrução 'while'."""
        _, condition, block = node
        print(f"Visiting 'while' statement with condition: {condition}")

        # Avaliar a condição do 'while'
        condition_value = self.visit(condition)

        # Verifica se a condição é um valor booleano
        if not isinstance(condition_value, bool):
            raise RuntimeError(f"Erro de tipo: a condição de 'while' deve ser um valor booleano, mas recebeu {type(condition_value)}.")

        # Processa o bloco do 'while'
        self.symbol_table.enter_scope()
        for stmt in block:
            self.visit(stmt)
        self.symbol_table.exit_scope()

    def visit_do_while(self, node):
        """Visita uma instrução 'do-while'."""
        _, block, condition = node
        print(f"Visiting 'do-while' statement with condition: {condition}")

        # Processa o bloco do 'do-while'
        self.symbol_table.enter_scope()
        for stmt in block:
            self.visit(stmt)
        self.symbol_table.exit_scope()

        # Avalia a condição após o bloco
        condition_value = self.visit(condition)

        # Verifica se a condição é um valor booleano
        if not isinstance(condition_value, bool):
            raise RuntimeError(f"Erro de tipo: a condição de 'do-while' deve ser um valor booleano, mas recebeu {type(condition_value)}.")

    def visit_for(self, node):
        """Visita uma instrução 'for'."""
        # Ajuste do desempacotamento do nó 'for'
        _, decl, condition, increment, block = node[0], node[1], node[2:5], node[5:7], node[7]

        print(f"Visiting 'for' loop with condition: {condition} and increment: {increment}")

        # Processa a declaração no início do 'for'
        self.visit(decl)

        # Avalia a condição do 'for'
        condition_value = self.visit(condition)

        # Verifica se a condição é um valor booleano
        if not isinstance(condition_value, bool):
            raise RuntimeError(f"Erro de tipo: a condição de 'for' deve ser um valor booleano, mas recebeu {type(condition_value)}.")

        # Processa o bloco do 'for'
        self.symbol_table.enter_scope()
        for stmt in block[1]:  # Assume que o bloco contém uma lista de declarações ou instruções
            self.visit(stmt)
        self.symbol_table.exit_scope()

        # Processa o incremento do 'for'
        self.visit(increment)


    def visit_comparison_operator(self, node):
        """Visita um operador de comparação (como <, >, ==)."""
        operator, left, right = node
        print(f"Visiting comparison operator: {operator} between {left} and {right}")

        # Verifica se 'left' é uma variável e obtém seu valor
        if isinstance(left, str):  # Se 'left' é uma string, então é uma variável
            left_value = self.symbol_table.get_symbol(left)["value"]
        else:
            # Caso contrário, é um valor literal
            left_value = self.visit(left)

        # Verifica se 'right' é uma variável
        if isinstance(right, str):  # Se 'right' é uma string, então é uma variável
            right_value = self.symbol_table.get_symbol(right)["value"]
        else:
            # Caso contrário, é um valor literal
            right_value = self.visit(right)

        # Verifica se ambos os lados são numéricos (int ou float)
        if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
            return left_value < right_value if operator == '<' else \
                left_value > right_value if operator == '>' else \
                left_value == right_value if operator == '==' else \
                False

        raise RuntimeError(f"Erro de tipo: operação de comparação inválida entre {type(left_value)} e {type(right_value)}.")

    def visit_function_call(self, node):
        _, function_name, parameters = node
        print(f"Visiting function call: {function_name} with parameters: {parameters}")

        # Verifica se a função foi declarada na tabela de símbolos
        function_symbol = self.symbol_table.get_symbol(function_name)
        if not function_symbol or "type" not in function_symbol or not function_symbol["type"].startswith("function"):
            raise RuntimeError(f"Erro: Função '{function_name}' não declarada.")

        # Processa os parâmetros da função
        param_values = [self.visit(param) for param in parameters]
        print(f"Function {function_name} called with {param_values}")
        return function_symbol["type"]  # Retorna o tipo da função

