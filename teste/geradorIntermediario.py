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
        elif len(parameter) == 2:  # ('parameter', NAME)
            _, param_name = parameter
            return param_name
    elif isinstance(parameter, str):  # Valor literal como strings
        return parameter
    raise ValueError(f"Unsupported parameter structure: {parameter}")

def process_expression(expression):
    """Processa expressões e retorna o nome do temporário que armazena o resultado."""
    if isinstance(expression, tuple):
        if len(expression) == 3:  # Operação binária: (op, left, right)
            op, left, right = expression
            temp_left = process_expression(left)
            temp_right = process_expression(right)
            temp_result = new_temp()
            intermediate_code.append(f"{temp_result} = {temp_left} {op} {temp_right}")
            return temp_result
        elif len(expression) == 2:  # Incremento ou decremento: (++ / --)
            op, operand = expression
            intermediate_code.append(f"{operand} = {operand} {op} 1")
            return operand
    elif isinstance(expression, (str, int, float)):  # Valores e variáveis
        return str(expression)
    else:
        raise ValueError(f"Unsupported expression: {expression}")

def process_declaration(content):
    """Processa declarações de variáveis."""
    if len(content) == 2:  # Tipo e nome da variável
        var_type, var_name = content
        intermediate_code.append(f"declare {var_type} {var_name}")
    elif len(content) == 3:  # Declaração com inicialização
        var_type, var_name, value = content
        intermediate_code.append(f"declare {var_type} {var_name}")
        temp = process_expression(value)
        intermediate_code.append(f"{var_name} = {temp}")
    elif len(content) == 4 and content[1] == "vector":  # Declaração de vetor
        var_type, _, vector_name = content
        intermediate_code.append(f"declare {var_type} {vector_name}[]")
    else:
        raise ValueError(f"Unsupported declaration structure: {content}")

def generate_code(node):
    """Função principal para percorrer a AST e gerar código intermediário."""
    if not node:
        return

    if isinstance(node, list):  # Lista de instruções
        for stmt in node:
            generate_code(stmt)
        return

    node_type, *content = node

    if node_type == 'expr_stmt':
        process_expression(content[0])

    elif node_type == 'declaration':
        process_declaration(content)

    elif node_type == 'preprocessor_directive':
        intermediate_code.append(f"directive {content[0]}")

    elif node_type == 'comment':
        pass  # Ignora comentários

    elif node_type == 'while':
        var, op, value, block = content
        label_start = new_label()
        label_end = new_label()
        intermediate_code.append(f"{label_start}:")
        temp = process_expression((op, var, value))
        intermediate_code.append(f"if_false {temp} goto {label_end}")
        generate_code(block)
        intermediate_code.append(f"goto {label_start}")
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'do_while':
        block, var, op, value = content
        label_start = new_label()
        intermediate_code.append(f"{label_start}:")
        generate_code(block)
        temp = process_expression((op, var, value))
        intermediate_code.append(f"if_false {temp} goto {label_start}")

    elif node_type == 'for':
        init, var, op, value, increment_var, increment_op, block = content
        label_start = new_label()
        label_end = new_label()
        generate_code(init)
        intermediate_code.append(f"{label_start}:")
        condition_temp = process_expression((op, var, value))
        intermediate_code.append(f"if_false {condition_temp} goto {label_end}")
        generate_code(block)
        process_expression((increment_op, increment_var))
        intermediate_code.append(f"goto {label_start}")
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'if':
        condition, block_then, *block_else = content
        label_else = new_label() if block_else else None
        label_end = new_label()
        condition_temp = process_expression(condition)
        intermediate_code.append(f"if_false {condition_temp} goto {label_else or label_end}")
        generate_code(block_then)
        if block_else:
            intermediate_code.append(f"goto {label_end}")
            intermediate_code.append(f"{label_else}:")
            generate_code(block_else[0])
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'return':
        temp = process_expression(content[0])
        intermediate_code.append(f"return {temp}")

    elif node_type == 'function_declaration':
        return_type, function_name, *rest = content
        parameters = rest[0] if len(rest) > 1 else []
        body = rest[-1]
        param_list = ", ".join([process_parameter(p) for p in parameters]) if parameters else ""
        intermediate_code.append(f"function {function_name}({param_list}) -> {return_type}")
        generate_code(body)
        intermediate_code.append(f"end_function {function_name}")

    elif node_type == 'block':
        for stmt in content[0]:
            generate_code(stmt)

    else:
        raise ValueError(f"Node type {node_type} not supported!")

def process_node(ast):
    """Gera o código intermediário baseado em uma AST."""
    global intermediate_code, temp_counter, label_counter
    intermediate_code = []
    temp_counter = 0
    label_counter = 0
    generate_code(ast)
    return "\n".join(intermediate_code)