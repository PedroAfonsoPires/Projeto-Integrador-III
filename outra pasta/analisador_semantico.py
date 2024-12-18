from symbol_table import SymbolTable

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
        print(f"Visitando nó: {node}")  # Log de debug detalhado

        if not node or not isinstance(node, tuple):
            print(f"Nó inválido ou desconhecido: {node}")
            return None

        method_name = f"visit_{node[0]}"
        print(f"Tentando chamar método: {method_name}")
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print(f"Warning: Nenhum visitador definido para o nó: {node[0]}")
        return None

    def visit_block(self, node):
        """Visita um bloco de código e processa suas instruções."""
        _, statements = node  # Exemplo: ('block', [instruções])
        for stmt in statements:
            self.visit(stmt)

    def visit_parameter(self, node):
        """Visita um nó de parâmetro."""
        _, param_type, *details = node

        # Identifica o nome do parâmetro e verifica ponteiros
        if len(details) == 1:
            param_name = details[0]
        elif len(details) == 2 and details[0] == '*':
            param_name = details[1]  # Nome do parâmetro após o '*'
            param_type = f"pointer({param_type})"
        else:
            raise RuntimeError(f"Formato de parâmetro inválido: {node}")

        print(f"Visiting parameter: {param_type} {param_name}")
        # Adiciona o parâmetro ao escopo atual na tabela de símbolos
        self.symbol_table.add_symbol(param_name, {"type": param_type, "value": None})
        self.report["symbols"].append({"name": param_name, "type": param_type, "value": None})

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
            self.symbol_table.add_symbol(vector_name, {"type": f"vector({var_type})", "value": None})
            self.report["symbols"].append({"name": vector_name, "type": f"vector({var_type})", "value": None})
            return {"name": vector_name, "type": f"vector({var_type})", "value": None}

        # Caso normal: variável simples
        if len(node) == 4:  # Se houver valor de inicialização
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
        value = node
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return value

    def check_type_compatibility(self, type1, type2):
        """Verifica a compatibilidade de tipos."""
        if type1 is None or type2 is None:
            raise RuntimeError("Erro de compatibilidade: um dos tipos é None.")

        if isinstance(type2, str):
            if type2.isdigit():
                type2 = int(type2)
            elif type2.replace('.', '', 1).isdigit() and type2.count('.') < 2:
                type2 = float(type2)

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

    def visit_function_declaration(self, node):
        """Visita uma declaração de função."""
        _, return_type, name, *params_and_block = node
        params = []
        block = None

        for item in params_and_block:
            if isinstance(item, tuple) and item[0] == 'parameter':
                params.append(item)
            elif isinstance(item, tuple) and item[0] == 'block':
                block = item

        print(f"Visiting function declaration: {name} with return type {return_type}")
        print(f"Parameters: {params}")

        self.symbol_table.add_symbol(name, {"type": f"function ({return_type})", "params": params})

        self.symbol_table.enter_scope()

        # Adiciona parâmetros ao escopo atual
        for param in params:
            self.visit(param)

        if block:
            self.visit(block)

        self.symbol_table.exit_scope()

    def visit_expr_stmt(self, node):
        """Visita uma instrução de expressão (por exemplo, atribuição ou operação)."""
        if len(node) != 4:
            raise RuntimeError(f"Estrutura inválida para expr_stmt: {node}")
        _, op, left, right = node
        print(f"Visitando expressão: {left} {op} {right}")
        left_value = self.visit(left)
        right_value = self.visit(right)

        if not self.check_type_compatibility(left_value, right_value):
            raise RuntimeError(f"Erro de tipo: {left} e {right} incompatíveis.")

    def visit_return(self, node):
        """Visita uma instrução de retorno."""
        if len(node) != 2:
            raise RuntimeError(f"Estrutura inválida para return: {node}")
        return_expr = node[1]
        print(f"Retornando expressão: {return_expr}")
        self.visit(return_expr)

    def visit_comment(self, node):
        """Ignora um comentário."""
        print(f"Ignorando comentário: {node[1]}")

    def visit_if(self, node):
        """Visita uma estrutura condicional 'if'."""
        if len(node) != 3:
            raise RuntimeError(f"Estrutura inválida para if: {node}")
        _, condition, block = node
        print(f"Visiting 'if' statement with condition: {condition}")
        condition_value = self.visit(condition)

        if not isinstance(condition_value, bool):
            raise RuntimeError("Erro de tipo: condição não é booleana.")

        self.visit(block)

    def visit_while(self, node):
        """Visita um laço 'while'."""
        if len(node) != 3:
            raise RuntimeError(f"Estrutura inválida para while: {node}")
        _, condition, block = node
        print(f"Visiting 'while' loop with condition: {condition}")
        condition_value = self.visit(condition)

        if not isinstance(condition_value, bool):
            raise RuntimeError("Erro de tipo: condição não é booleana.")

        self.visit(block)

    def visit_do_while(self, node):
        """Visita um laço 'do-while'."""
        if len(node) != 3:
            raise RuntimeError(f"Estrutura inválida para do-while: {node}")
        _, block, condition = node
        print(f"Visiting 'do-while' loop with condition: {condition}")
        self.visit(block)
        condition_value = self.visit(condition)

        if not isinstance(condition_value, bool):
            raise RuntimeError("Erro de tipo: condição não é booleana.")

    def visit_for(self, node):
        """Visita um laço 'for'."""
        if len(node) != 5:
            raise RuntimeError(f"Estrutura inválida para for: {node}")
        _, init, condition, increment, block = node
        print(f"Visiting 'for' loop")
        self.visit(init)
        self.visit(condition)
        self.visit(increment)
        self.visit(block)

    def visit_comparison_operator(self, node):
        """Visita um operador de comparação."""
        if len(node) != 3:
            raise RuntimeError(f"Estrutura inválida para comparison_operator: {node}")
        operator, left, right = node
        print(f"Visiting comparison operator: {operator} between {left} and {right}")
        left_value = self.visit(left)
        right_value = self.visit(right)
        return operator in ('<', '>', '==', '!=', '<=', '>=') and isinstance(left_value, (int, float)) and isinstance(right_value, (int, float))

    def get_all_symbols(self):
        """Retorna todos os símbolos da tabela de símbolos."""
        return self.symbol_table