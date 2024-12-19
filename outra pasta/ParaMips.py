registers = [f"$t{i}" for i in range(8)]  # 8 registradores disponíveis
register_map = {}  # Mapear temporários para registradores
memory_map = {}  # Mapear variáveis para endereços de memória
current_memory_address = 0
mips_code = []

def allocate_register(temp):
    """Atribui um registrador a um temporário ou variável."""
    global current_memory_address

    if temp.isdigit():  # Se é uma constante literal
        return temp

    if temp in register_map:  # Se já está mapeado para um registrador
        return register_map[temp]

    # Procurar registradores livres
    for reg in registers:
        if reg not in register_map.values():
            register_map[temp] = reg
            return reg

    # Se todos os registradores estão ocupados, desalocar o primeiro mapeado
    spilled_var = list(register_map.keys())[0]
    spilled_reg = register_map[spilled_var]
    if spilled_var not in memory_map:
        memory_map[spilled_var] = current_memory_address
        current_memory_address += 4
    mips_code.append(f"sw {spilled_reg}, {memory_map[spilled_var]}($sp)")
    del register_map[spilled_var]

    # Alocar o registrador desalocado para o novo temporário/variável
    register_map[temp] = spilled_reg
    return spilled_reg

def process_intermediate_to_mips(intermediate_code):
    """Converte código intermediário para MIPS simplificado."""
    global mips_code, register_map, memory_map, current_memory_address
    mips_code = []
    register_map = {}
    memory_map = {}
    current_memory_address = 0

    for line in intermediate_code:
        tokens = line.split()
        if "=" in tokens:
            # Atribuições
            dest, _, src1, *rest = tokens
            reg_dest = allocate_register(dest)

            if len(rest) == 2:  # Operação binária
                operator, src2 = rest
                reg_src1 = allocate_register(src1)

                if src2.isdigit():
                    # src2 é uma constante
                    if operator == "+":
                        mips_code.append(f"addi {reg_dest}, {reg_src1}, {src2}")
                    elif operator == "-":
                        mips_code.append(f"addi {reg_dest}, {reg_src1}, -{src2}")
                else:
                    # src2 é um registrador ou variável
                    reg_src2 = allocate_register(src2)
                    if operator == "+":
                        mips_code.append(f"add {reg_dest}, {reg_src1}, {reg_src2}")
                    elif operator == "-":
                        mips_code.append(f"sub {reg_dest}, {reg_src1}, {reg_src2}")
                    elif operator == "and":
                        mips_code.append(f"and {reg_dest}, {reg_src1}, {reg_src2}")
                    elif operator == "or":
                        mips_code.append(f"or {reg_dest}, {reg_src1}, {reg_src2}")

            elif len(rest) == 0:  # Atribuição simples
                if src1.isdigit():  # Se é um número
                    mips_code.append(f"addi {reg_dest}, $zero, {src1}")
                else:  # Se é uma variável ou registrador
                    reg_src1 = allocate_register(src1)
                    mips_code.append(f"addi {reg_dest}, {reg_src1}, 0")

        elif "if_false" in line:
            # Condições
            _, temp, _, label = tokens
            reg = allocate_register(temp)
            mips_code.append(f"beq {reg}, $zero, {label}")

        elif "goto" in line:
            # Goto
            _, label = tokens
            mips_code.append(f"j {label}")

        elif ":" in line:
            # Rótulos
            mips_code.append(line)

        elif "return" in line:
            # Retorno
            _, temp = tokens
            reg = allocate_register(temp)
            mips_code.append(f"move $v0, {reg}")

        elif "declare" in line:
            # Declaração
            _, var_type, var_name = tokens[:3]
            if len(tokens) > 3:  # Vetor
                memory_map[var_name] = current_memory_address
                current_memory_address += 4 * int(tokens[3])
            else:
                memory_map[var_name] = current_memory_address
                current_memory_address += 4

        elif "load" in line:
            # Carregamento em estilo C: value = *ptr;
            _, ptr, dest = tokens
            reg_ptr = allocate_register(ptr)
            reg_dest = allocate_register(dest)
            mips_code.append(f"lw {reg_dest}, 0({reg_ptr})")

        elif "store" in line:
            # Armazenamento em estilo C: *ptr = value;
            _, src, ptr = tokens
            reg_src = allocate_register(src)
            reg_ptr = allocate_register(ptr)
            mips_code.append(f"sw {reg_src}, 0({reg_ptr})")

        elif "directive" in line:
            # Diretivas
            mips_code.append(f"# {line}")

    return "\n".join(mips_code)
