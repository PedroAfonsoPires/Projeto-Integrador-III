intermediate_code = []  # Armazena as instruções do código intermediário
temp_counter = 0
label_counter = 0


def new_temp():
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"


def new_label():
    global label_counter
    label_counter += 1
    return f"L{label_counter}"


def generate_code(node):
    """Função principal para percorrer a AST e gerar código intermediário."""
    if not node:
        return

    if isinstance(node, list):  # Lista de declarações ou instruções
        for stmt in node:
            generate_code(stmt)
        return

    if isinstance(node, tuple) and len(node) == 2 and isinstance(node[1], tuple):
        # Nó estruturado, ex: ('expr_stmt', ('=', 'n', '0'))
        node_type, content = node
    else:
        node_type = node[0]
        content = node[1:] if len(node) > 1 else None

    if node_type == 'expr_stmt':
        temp = process_expression(content)
        intermediate_code.append(f"{temp}")

    elif node_type == 'declaration':
        if len(content) == 2:  # TYPE ID
            var_type, var_name = content
            intermediate_code.append(f"declare {var_type} {var_name}")
        elif len(content) == 3:  # TYPE ID = expression
            var_type, var_name, expression = content
            temp = process_expression(expression)
            intermediate_code.append(f"{var_name} = {temp}")

    elif node_type == 'if':
        condition, block_then, *block_else = content
        label_else = new_label() if block_else else None
        label_end = new_label()
        temp = process_expression(condition)
        intermediate_code.append(f"if_false {temp} goto {label_else or label_end}")
        generate_code(block_then)
        if block_else:
            intermediate_code.append(f"goto {label_end}")
            intermediate_code.append(f"{label_else}:")
            generate_code(block_else[0])
        intermediate_code.append(f"{label_end}:")

    elif node_type == 'block':
        generate_code(content)  # Bloco pode ser uma lista de instruções

    elif node_type == 'return':
        temp = process_expression(content[0])
        intermediate_code.append(f"return {temp}")

    else:
        raise ValueError(f"Node type {node_type} not supported!")

def process_expression(expression):
    """Processa expressões e retorna o nome do temporário que armazena o resultado."""
    if isinstance(expression, tuple):  # Operação binária ou atribuição
        op, left, right = expression
        temp1 = process_expression(left)
        temp2 = process_expression(right)
        temp_result = new_temp()
        intermediate_code.append(f"{temp_result} = {temp1} {op} {temp2}")
        return temp_result
    elif isinstance(expression, str):  # Variável ou valor literal
        return expression
    elif isinstance(expression, int) or isinstance(expression, float):  # Número
        temp = new_temp()
        intermediate_code.append(f"{temp} = {expression}")
        return temp
    else:
        raise ValueError(f"Expression {expression} not supported!")


def process_node(ast):
    """Função chamada no main.py para gerar código intermediário."""
    global intermediate_code, temp_counter, label_counter
    intermediate_code = []
    temp_counter = 0
    label_counter = 0
    generate_code(ast)
    return "\n".join(intermediate_code)
