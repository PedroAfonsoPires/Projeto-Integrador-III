class SymbolTable:
    def __init__(self, raw_table=None, filename=None):
        # Inicializa a tabela de símbolos vazia se não for fornecida
        self.raw_table = raw_table if raw_table is not None else {}
        self.filename = filename
        self.current_scope = [{}]  # Escopos empilhados para o controle de blocos

    def add_symbol(self, name, attributes):
        """Adiciona um símbolo na tabela."""
        if name in self.current_scope[-1]:
            raise RuntimeError(f"Erro: '{name}' já declarado no escopo atual.")
        self.current_scope[-1][name] = attributes

    def get_symbol(self, name):
        """Busca um símbolo na tabela, respeitando os escopos."""
        for scope in reversed(self.current_scope):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Erro: '{name}' não declarado.")

    def enter_scope(self):
        """Entra em um novo escopo."""
        self.current_scope.append({})

    def exit_scope(self):
        """Sai do escopo atual."""
        if len(self.current_scope) == 1:
            raise RuntimeError("Erro: Tentativa de sair do escopo global.")
        self.current_scope.pop()