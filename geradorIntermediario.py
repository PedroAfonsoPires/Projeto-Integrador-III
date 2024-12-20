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
    """Processa um parâmetro e retorna sua representação como string."""
    #print(parameter)
    if isinstance(parameter, tuple):
        if parameter[0] == 'parameter':
            # Caso simples: parâmetro como ('parameter', 'int')
            if len(parameter) == 2 or len(parameter):
                return parameter[1]
            # Parâmetro com tipo e modificador, como ('parameter', 'int', '*', 'a')
            elif len(parameter) == 3:
                return f"{parameter[1]} {parameter[2]}"
            # Parâmetro com tipo, modificador e mais um nível de estrutura, como ('parameter', 'int', '*', 'a', ('parameter', 'int', '*', 'b'))
            elif len(parameter) == 4:
                return f"{parameter[1]} {parameter[2]} {process_parameter(parameter[3])}"
            elif len(parameter) == 5:
                # Este caso trata de ponteiros de ponteiros (e mais níveis)
                pointer_type = f"{parameter[1]} {parameter[2]}"
                nested_parameter = process_parameter(parameter[4])  # Processa o parâmetro aninhado
                return f"{pointer_type} {nested_parameter}"
            else:
                raise ValueError(f"Unsupported parameter structure: {parameter}")
        else:
            raise ValueError(f"Unsupported parameter structure: {parameter}")
    elif parameter is None:
        return ""  # Retorna uma string vazia
    else:
        raise ValueError(f"Unsupported parameter type: {parameter}")



def process_expression(expression, current_scope, symbol_table):
    """Processa expressões e retorna o nome do temporário que armazena o resultado."""
    if isinstance(expression, tuple):
        if len(expression) == 3:  # Operação binária: (op, left, right)
            op, left, right = expression

            if op == '*':  # Multiplicação por somas sucessivas
                temp_result = new_temp()
                temp_index = new_temp()
                temp_left = process_expression(left, current_scope, symbol_table)
                temp_right = process_expression(right, current_scope, symbol_table)

                # Inicializa o acumulador e o índice
                intermediate_code.append(f"{temp_result} = 0")
                intermediate_code.append(f"{temp_index} = 0")

                # Loop de adição
                loop_start = new_label()
                loop_end = new_label()
                intermediate_code.append(f"{loop_start}:")
                intermediate_code.append(f"if {temp_index} >= {temp_right} goto {loop_end}")
                intermediate_code.append(f"{temp_result} = {temp_result} + {temp_left}")
                intermediate_code.append(f"{temp_index} = {temp_index} + 1")
                intermediate_code.append(f"goto {loop_start}")
                intermediate_code.append(f"{loop_end}:")

                return temp_result

            elif op == '/':  # Divisão por subtrações sucessivas
                temp_result = new_temp()
                temp_remainder = new_temp()
                temp_left = process_expression(left, current_scope, symbol_table)
                temp_right = process_expression(right, current_scope, symbol_table)

                # Inicializa o quociente e o resto
                intermediate_code.append(f"{temp_result} = 0")
                intermediate_code.append(f"{temp_remainder} = {temp_left}")

                # Loop de subtração
                loop_start = new_label()
                loop_end = new_label()
                intermediate_code.append(f"{loop_start}:")
                intermediate_code.append(f"if {temp_remainder} < {temp_right} goto {loop_end}")
                intermediate_code.append(f"{temp_remainder} = {temp_remainder} - {temp_right}")
                intermediate_code.append(f"{temp_result} = {temp_result} + 1")
                intermediate_code.append(f"goto {loop_start}")
                intermediate_code.append(f"{loop_end}:")

                return temp_result

            else:  # Outros operadores
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
        #symbol_table.add_symbol(var_name, {"type": var_type})
        intermediate_code.append(f"declare {var_type} {var_name}")
        temp = process_expression(value, current_scope, symbol_table)
        intermediate_code.append(f"{var_name} = {temp}")
    elif len(content) == 5 and content[1] == "vector":  # Declaração de vetor
        var_type, _, vector_name, array_initializer, values = content
        if array_initializer == "array_initializer":
            # Declaração do vetor
            symbol_table.add_symbol(vector_name, {"type": f"{var_type}[]"})
            intermediate_code.append(f"declare {var_type} {vector_name}[]")
            # Atribuindo valores para o vetor
            for index, value in enumerate(values):
                temp = process_expression(value, current_scope, symbol_table)
                intermediate_code.append(f"{vector_name}[{index}] = {temp}")
        else:
            raise ValueError(f"Unsupported vector initialization: {array_initializer}")
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
        content_len = len(content)

        if (content_len == 7 and content[0][0] == 'declaration'):
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

        elif (content_len == 7 and content[0][0] != 'declaration'):
            init, var, op, value, increment_var, increment_op, block = content
            label_start = new_label()
            label_end = new_label()

            # O laço começa sem uma inicialização explícita, pois a variável `n` já foi inicializada anteriormente
            intermediate_code.append(f"{label_start}:")

            # Gerar código intermediário para a condição: n > 0
            condition_temp = process_expression((op, var, value), current_scope, symbol_table)
            intermediate_code.append(f"if_false {condition_temp} goto {label_end}")

            # Processar o bloco dentro do laço (mesmo que vazio)
            symbol_table.enter_scope()
            generate_code(block, current_scope, symbol_table)
            symbol_table.exit_scope()

            # Gerar o código intermediário para o decremento: n--
            process_expression((increment_op, increment_var), current_scope, symbol_table)

            intermediate_code.append(f"goto {label_start}")
            intermediate_code.append(f"{label_end}:")

        elif content_len == 9:  # Caso de um 'for' com inicialização, condição e decremento (9 elementos)
            var_name, eq, var_value, var_cond, op, cond_value, var_increment, increment, block = content

            # Inicialização da variável
            intermediate_code.append(f"{var_name} = {var_value}")

            label_start = new_label()
            label_end = new_label()

            # Gerar o código do laço 'for'
            intermediate_code.append(f"{label_start}:")

            # Condição do laço
            condition_temp = process_expression((op, var_name, cond_value), current_scope, symbol_table)
            intermediate_code.append(f"if_false {condition_temp} goto {label_end}")

            # Processar o bloco (no caso, incremento n++)
            symbol_table.enter_scope()
            generate_code(block, current_scope, symbol_table)
            symbol_table.exit_scope()

            # Decremento (n--)
            intermediate_code.append(f"{var_name} = {var_name} - 1")

            intermediate_code.append(f"goto {label_start}")
            intermediate_code.append(f"{label_end}:")





        else:
            raise ValueError(f"Erro na estrutura do 'for', quantidade de elementos inesperada: {content_len}.")

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
