class SymbolTable:
    def __init__(self, raw_table=None, filename=None):
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


intermediate_code = []  # Armazena as instruções do código intermediário
temp_counter = 0
label_counter = 0

def new_temp():
    """Gera um novo temporário t1, t2, ..."""
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

def new_label():
    """Gera um novo rótulo L1, L2, ..."""
    global label_counter
    label_counter += 1
    return f"L{label_counter}"

def process_parameter(parameter):
    """Processa um parâmetro e retorna sua representação no código intermediário."""
    if isinstance(parameter, tuple):
        if len(parameter) == 3:  # ('parameter', TYPE, NAME)
            _, param_type, param_name = parameter
            return f"{param_type} {param_name}"
        elif len(parameter) == 4:  # ('parameter', TYPE, '*', NAME) para ponteiros
            _, param_type, _, param_name = parameter
            return f"{param_type}* {param_name}"
        elif len(parameter) == 5 and isinstance(parameter[4], tuple):  # Parâmetro composto
            _, param_type, _, param_name, sub_param = parameter
            sub_param_str = process_parameter(sub_param)
            return f"{param_type}* {param_name}, {sub_param_str}"
    elif isinstance(parameter, str):  # Valor literal como strings
        return parameter
    raise ValueError(f"Unsupported parameter structure: {parameter}")

def process_expression(expression, current_scope, symbol_table):
    """Processa expressões e retorna o nome do temporário que armazena o resultado."""
    if isinstance(expression, tuple):
        if len(expression) == 3:  # Operação binária: (op, left, right)
            op, left, right = expression
            temp_left = process_expression(left, current_scope, symbol_table)
            temp_right = process_expression(right, current_scope, symbol_table)
            temp_result = new_temp()
            intermediate_code.append(f"{temp_result} = {temp_left} {op} {temp_right}")
            return temp_result
        elif len(expression) == 2:  # Incremento ou decremento: (++ / --)
            op, operand = expression
            temp_operand = process_expression(operand, current_scope, symbol_table)
            intermediate_code.append(f"{operand} = {temp_operand} {op} 1")
            return operand
    elif isinstance(expression, str):  # Valores e variáveis
        try:
            symbol_table.get_symbol(expression)  # Verifica se é uma variável
            return expression
        except RuntimeError:  # Caso contrário, é um valor literal
            return str(expression)
    else:
        raise ValueError(f"Unsupported expression: {expression}")

def process_declaration(content, current_scope, symbol_table):
    """Processa declarações de variáveis usando a tabela de símbolos."""
    if len(content) == 2:  # Tipo e nome da variável
        var_type, var_name = content
        symbol_table.add_symbol(var_name, {"type": var_type})
        intermediate_code.append(f"declare {var_type} {var_name}")
    elif len(content) == 3:  # Declaração com inicialização
        var_type, var_name, value = content
        symbol_table.add_symbol(var_name, {"type": var_type})
        intermediate_code.append(f"declare {var_type} {var_name}")
        temp = process_expression(value, current_scope, symbol_table)
        intermediate_code.append(f"{var_name} = {temp}")
    elif len(content) == 4 and content[1] == "vector":  # Declaração de vetor
        var_type, _, vector_name = content
        symbol_table.add_symbol(vector_name, {"type": f"{var_type}[]"})
        intermediate_code.append(f"declare {var_type} {vector_name}[]")
    else:
        raise ValueError(f"Unsupported declaration structure: {content}")

def generate_code(node, current_scope, symbol_table):
    """Função principal para percorrer a AST e gerar código intermediário."""
    if not node:
        return

    if isinstance(node, list):  # Lista de instruções
        for stmt in node:
            generate_code(stmt, current_scope, symbol_table)
        return

    node_type, *content = node

    if node_type == 'expr_stmt':
        process_expression(content[0], current_scope, symbol_table)

    elif node_type == 'declaration':
        process_declaration(content, current_scope, symbol_table)

    elif node_type == 'preprocessor_directive':
        intermediate_code.append(f"directive {content[0]}")

    elif node_type == 'comment':
        pass  # Ignora comentários

    elif node_type == 'while':
        var, op, value, block = content
        label_start = new_label()
        label_end = new_label()
        intermediate_code.append(f"{label_start}:")
        temp = process_expression((op, var, value), current_scope, symbol_table)
        intermediate_code.append(f"if_false {temp} goto {label_end}")
        symbol_table.enter_scope()
        generate_code(block, current_scope, symbol_table)
        symbol_table.exit_scope()
        intermediate_code.append(f"goto {label_start}")
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'do_while':
        block, var, op, value = content
        label_start = new_label()
        intermediate_code.append(f"{label_start}:")
        symbol_table.enter_scope()
        generate_code(block, current_scope, symbol_table)
        symbol_table.exit_scope()
        temp = process_expression((op, var, value), current_scope, symbol_table)
        intermediate_code.append(f"if_false {temp} goto {label_start}")

    elif node_type == 'for':
        init, var, op, value, increment_var, increment_op, block = content
        label_start = new_label()
        label_end = new_label()
        generate_code(init, current_scope, symbol_table)
        intermediate_code.append(f"{label_start}:")
        condition_temp = process_expression((op, var, value), current_scope, symbol_table)
        intermediate_code.append(f"if_false {condition_temp} goto {label_end}")
        symbol_table.enter_scope()
        generate_code(block, current_scope, symbol_table)
        symbol_table.exit_scope()
        process_expression((increment_op, increment_var), current_scope, symbol_table)
        intermediate_code.append(f"goto {label_start}")
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'if':
        condition, block_then, *block_else = content
        label_else = new_label() if block_else else None
        label_end = new_label()
        condition_temp = process_expression(condition, current_scope, symbol_table)
        intermediate_code.append(f"if_false {condition_temp} goto {label_else or label_end}")
        symbol_table.enter_scope()
        generate_code(block_then, current_scope, symbol_table)
        symbol_table.exit_scope()
        if block_else:
            intermediate_code.append(f"goto {label_end}")
            intermediate_code.append(f"{label_else}:")
            symbol_table.enter_scope()
            generate_code(block_else[0], current_scope, symbol_table)
            symbol_table.exit_scope()
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'return':
        temp = process_expression(content[0], current_scope, symbol_table)
        intermediate_code.append(f"return {temp}")

    elif node_type == 'function_declaration':
        return_type, function_name, *rest = content
        func_info = symbol_table.get_symbol(function_name)
        parameters = func_info.get('params', [])
        param_list = ", ".join([process_parameter(p) for p in parameters]) if parameters else ""
        intermediate_code.append(f"function {function_name}({param_list}) -> {return_type}")
        symbol_table.enter_scope()
        generate_code(rest[-1], function_name, symbol_table)
        symbol_table.exit_scope()
        intermediate_code.append(f"end_function {function_name}")

    elif node_type == 'block':
        symbol_table.enter_scope()
        for stmt in content[0]:
            generate_code(stmt, current_scope, symbol_table)
        symbol_table.exit_scope()

    else:
        raise ValueError(f"Node type {node_type} not supported!")

def process_node(ast, symbol_table):
    """Gera o código intermediário baseado em uma AST e uma Tabela de Símbolos."""
    global intermediate_code, temp_counter, label_counter
    intermediate_code = []
    temp_counter = 0
    label_counter = 0
    generate_code(ast, 1, symbol_table)  # Começa no escopo global (1)
    return "\n".join(intermediate_code)
