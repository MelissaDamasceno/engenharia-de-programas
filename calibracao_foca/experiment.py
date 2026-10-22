from time import time

def run_assignment_experiment(lista_n, R):
    """Executa a medição de tempos de atribuição (x = i)"""
    print("Coletando medições de tempo para Atribuição (x = i)...")
    TAU_A = []
    for n in lista_n:
        tt = []
        for r in range(R):
            t = 0
            for i in range(n):
                tic = time()
                x = i
                toc = time()
                t += toc - tic
            tt.append(t / n)  # tempo medio por iteracao nesta repeticao
        TAU_A.append(tt)
    return TAU_A

def run_operation_experiment(lista_n, R, TAU_A=None):
    """Executa a medição de tempos de operação (x = a + b).
    Se TAU_A for fornecido, a baseline será subtraída."""
    a = 1
    b = 2
    TAU_O_BRUTO = []     # Operação + Atribuição (x = a + b)
    TAU_O_ISOLADO = []   # Operação isolada ( (x = a + b) - (x = a) )

    print("Coletando medições de tempo para Operação (x = a + b)...")
    for idx_n, n in enumerate(lista_n):
        tt_op_bruto = []
        tt_op_isolado = []
        for r in range(R):
            t = 0
            for i in range(n):
                tic = time()
                x = a + b
                toc = time()
                t += toc - tic
            tempo_medio = t / n
            tt_op_bruto.append(tempo_medio)
            
            if TAU_A is not None:
                # Subtrai a baseline de atribuição da mesma repetição r
                tempo_atrib = TAU_A[idx_n][r]
                tt_op_isolado.append(max(0.0, tempo_medio - tempo_atrib))
            else:
                tt_op_isolado.append(tempo_medio)
            
        TAU_O_BRUTO.append(tt_op_bruto)
        TAU_O_ISOLADO.append(tt_op_isolado)
        
    return TAU_O_BRUTO, TAU_O_ISOLADO

def run_comparison_experiment(lista_n, R, TAU_A=None):
    """Executa a medição de tempos de comparação (if a < b / if a < CONSTANTE).

    A comparação é sempre verdadeira, e o `toc = time()` fica dentro do `if`,
    de modo que o tempo medido é (comparação + atribuição).
    Se TAU_A for fornecido, a baseline de atribuição será subtraída.
    """
    a = 1
    b = 2
    CONSTANTE = 2

    TAU_C_VAR_BRUTO = []      # Comparação com variável + Atribuição (if a < b)
    TAU_C_VAR_ISOLADO = []    # Comparação com variável isolada
    TAU_C_CONST_BRUTO = []    # Comparação com constante + Atribuição (if a < 2)
    TAU_C_CONST_ISOLADO = []  # Comparação com constante isolada

    print("Coletando medições de tempo para Comparação (if a < b / if a < CONSTANTE)...")
    for idx_n, n in enumerate(lista_n):
        tt_var_bruto = []
        tt_var_isolado = []
        tt_const_bruto = []
        tt_const_isolado = []
        for r in range(R):
            # Comparação entre variáveis (a < b)
            t = 0
            for i in range(n):
                tic = time()
                if a < b:
                    toc = time()
                t += toc - tic
            tempo_medio_var = t / n

            # Comparação entre variável e constante (a < 2)
            t = 0
            for i in range(n):
                tic = time()
                if a < CONSTANTE:
                    toc = time()
                t += toc - tic
            tempo_medio_const = t / n

            tt_var_bruto.append(tempo_medio_var)
            tt_const_bruto.append(tempo_medio_const)

            if TAU_A is not None:
                # Subtrai a baseline de atribuição da mesma repetição r
                tempo_atrib = TAU_A[idx_n][r]
                tt_var_isolado.append(max(0.0, tempo_medio_var - tempo_atrib))
                tt_const_isolado.append(max(0.0, tempo_medio_const - tempo_atrib))
            else:
                tt_var_isolado.append(tempo_medio_var)
                tt_const_isolado.append(tempo_medio_const)

        TAU_C_VAR_BRUTO.append(tt_var_bruto)
        TAU_C_VAR_ISOLADO.append(tt_var_isolado)
        TAU_C_CONST_BRUTO.append(tt_const_bruto)
        TAU_C_CONST_ISOLADO.append(tt_const_isolado)

    return TAU_C_VAR_BRUTO, TAU_C_VAR_ISOLADO, TAU_C_CONST_BRUTO, TAU_C_CONST_ISOLADO
