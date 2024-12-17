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
        if len(node) == 4:  # Inicialização
            value = self.visit(node[3])
            if not self.check_type_compatibility(var_type, value):
                raise RuntimeError(f"Incompatibilidade de tipos ao inicializar '{var_name}'.")
        self.symbol_table.add_symbol(var_name, {"type": var_type})
        self.report["symbols"].append({"name": var_name, "type": var_type})
        return {"name": var_name, "type": var_type, "value": value}

    def visit_literal(self, node):
        """Visita um valor literal e retorna seu tipo."""
        return node[0]  # Simplesmente retorna o tipo literal para valores como '10'

    def check_type_compatibility(self, type1, type2):
        """Verifica a compatibilidade de tipos."""
        if type1 is None or type2 is None:
            raise RuntimeError("Erro de compatibilidade: um dos tipos é None.")
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

    def get_all_symbols(self):
        return self.symbol_table
