class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Lista de escopos (pilha de dicionários)

    def enter_scope(self):
        """Entra em um novo escopo."""
        self.scopes.append({})

    def exit_scope(self):
        """Sai do escopo atual."""
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise RuntimeError("Tentativa de sair do escopo global.")

    def add_symbol(self, name, value):
        """Adiciona um símbolo ao escopo atual."""
        if name in self.scopes[-1]:
            raise RuntimeError(f"Símbolo '{name}' já declarado no escopo atual.")
        self.scopes[-1][name] = value

    def get_symbol(self, name):
        """Obtém o símbolo do escopo mais próximo."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Símbolo '{name}' não declarado.")


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
        method_name = f"visit_{node[0]}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise RuntimeError(f"Nenhum visitador definido para o nó: {node[0]}")

    def visit_declaration(self, node):
        """Visita uma declaração de variável."""
        _, var_type, var_name = node[:3]
        if len(node) == 4:  # Inicialização
            value = self.visit(node[3])
            if not self.check_type_compatibility(var_type, value):
                raise RuntimeError(f"Incompatibilidade de tipos ao inicializar '{var_name}'.")
        self.symbol_table.add_symbol(var_name, {"type": var_type})
        self.report["symbols"].append({"name": var_name, "type": var_type})

    def visit_expr_stmt(self, node):
        """Visita uma expressão em um statement."""
        return self.visit(node[1])

    def visit_expression(self, node):
        """Visita uma expressão e verifica tipos."""
        if len(node) == 3:  # Operação binária
            left = self.visit(node[1])
            right = self.visit(node[2])
            if not self.check_type_compatibility(left, right):
                raise RuntimeError(f"Incompatibilidade de tipos em expressão: {left} e {right}.")
            return left  # Retorna o tipo resultante
        elif len(node) == 2:  # Operação unária
            operand = self.visit(node[1])
            return operand
        else:  # Identificador ou número
            return node

    def visit_function_declaration(self, node):
        """Visita uma declaração de função."""
        _, return_type, func_name, params, body = node
        self.symbol_table.add_symbol(func_name, {"type": return_type, "params": params})
        self.report["symbols"].append({"name": func_name, "type": return_type, "params": params})
        self.symbol_table.enter_scope()
        for param_type, param_name in params:
            self.symbol_table.add_symbol(param_name, {"type": param_type})
            self.report["symbols"].append({"name": param_name, "type": param_type})
        self.visit(body)
        self.symbol_table.exit_scope()

    def visit_function_call(self, node):
        """Visita uma chamada de função."""
        _, func_name, args = node
        func_symbol = self.symbol_table.get_symbol(func_name)
        if len(args) != len(func_symbol["params"]):
            raise RuntimeError(f"Número de argumentos inválido para a função '{func_name}'.")
        for arg, param in zip(args, func_symbol["params"]):
            if not self.check_type_compatibility(self.visit(arg), param["type"]):
                raise RuntimeError(f"Tipo incompatível no argumento '{arg}' da função '{func_name}'.")

    def visit_block(self, node):
        """Visita um bloco de código."""
        _, statements = node
        self.symbol_table.enter_scope()
        for statement in statements:
            self.visit(statement)
        self.symbol_table.exit_scope()

    def check_type_compatibility(self, type1, type2):
        """Verifica a compatibilidade de tipos."""
        return type1 == type2

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