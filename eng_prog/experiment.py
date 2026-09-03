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
