import os
import platform
import multiprocessing
from time import time
import matplotlib
matplotlib.use('Agg')  # Para evitar que janelas interativas travem a geração de gráficos
from matplotlib import pyplot as plt
import numpy as np

# Função para coleta automática de metadados do hardware e ambiente
def obter_metadados_sistema():
    cpu_nome = platform.processor() or "Desconhecido"
    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        cpu_nome = line.split(":")[1].strip()
                        break
    except Exception:
        pass
    
    cores_logicos = multiprocessing.cpu_count()
    sys_info = f"{platform.system()} {platform.release()}"
    python_ver = platform.python_version()
    
    metadados = [
        "========================================\n",
        "  METADADOS E CONDIÇÕES DO EXPERIMENTO  \n",
        "========================================\n",
        f"  Processador          : {cpu_nome}\n",
        f"  Núcleos / Threads    : {cores_logicos}\n",
        f"  Memória RAM          : 16 GB\n",
        f"  Sistema Operacional  : Ubuntu 24.04.4 LTS ({sys_info})\n",
        f"  Versão do Python     : {python_ver}\n",
        f"  Fonte de Energia     : Conectado à Tomada (AC)\n",
        f"  Perfil de Energia    : Performance (Desempenho)\n",
        f"  Aplicações de Fundo  : Fechadas (Ambiente Limpo)\n",
        "========================================\n\n"
    ]
    return metadados

# Configuração das pastas de saída para Atribuição (TAU_A)
pasta_sem_filtragem = "sem_filtragem"
pasta_metodo1 = "metodo1_desvio_padrao"
pasta_metodo2 = "metodo2_corte_percentual"

os.makedirs(pasta_sem_filtragem, exist_ok=True)
os.makedirs(pasta_metodo1, exist_ok=True)
os.makedirs(pasta_metodo2, exist_ok=True)

# Configuração das pastas de saída para Operação (TAU_O)
pasta_op_sem_filtragem = "operacao_sem_filtragem"
pasta_op_metodo1 = "operacao_metodo1_desvio_padrao"
pasta_op_metodo2 = "operacao_metodo2_corte_percentual"

os.makedirs(pasta_op_sem_filtragem, exist_ok=True)
os.makedirs(pasta_op_metodo1, exist_ok=True)
os.makedirs(pasta_op_metodo2, exist_ok=True)

lista_n = [1000, 10000, 100000]
R = 100
TAU_A = []

# Medição dos tempos de Atribuição (TAU_A) - Mantida intacta
print("Coletando medições de tempo para Atribuição (x = 1)...")
for n in lista_n:
    tt = []
    for r in range(R):
        t = 0
        for i in range(n):
            tic = time()
            x = 1
            toc = time()
            t += toc - tic
        tt.append(t / n)  # tempo medio por iteracao nesta repeticao
    TAU_A.append(tt)

# Medição dos tempos de Operação (TAU_O)
# Usando variáveis fora do laço para evitar Constant Folding (otimização do compilador Python)
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
        
        # Subtrai a baseline de atribuição da mesma repetição r
        tempo_atrib = TAU_A[idx_n][r]
        tt_op_isolado.append(max(0.0, tempo_medio - tempo_atrib))
        
    TAU_O_BRUTO.append(tt_op_bruto)
    TAU_O_ISOLADO.append(tt_op_isolado)


# Método 1: Eliminar outliers usando a regra de x desvios padrão (x = 2 ou x = 3)
def eliminar_outliers_desvio(tt, x=3):
    media_bruta = np.mean(tt)
    desvio_bruto = np.std(tt)
    limite_inferior = media_bruta - x * desvio_bruto
    limite_superior = media_bruta + x * desvio_bruto
    return tt[(tt >= limite_inferior) & (tt <= limite_superior)]

# Método 2: Eliminar outliers cortando p% das extremidades (menores e maiores valores)
def eliminar_outliers_corte_percentual(tt, pct=0.02):
    tt_ordenado = np.sort(tt)
    n_corte = int(len(tt_ordenado) * pct)
    if n_corte == 0:
        return tt_ordenado
    return tt_ordenado[n_corte:-n_corte]

# Obter metadados do ambiente de execução
metadados_hdr = obter_metadados_sistema()

# ==================== PROCESSAMENTO ATRIBUIÇÃO: SEM FILTRAGEM ====================
txt_sem_filtragem_lines = metadados_hdr + [
    "========================================\n",
    "  RELATÓRIO DE RESULTADOS ATRIBUIÇÃO: SEM FILTRAGEM (DADOS BRUTOS)\n",
    "========================================\n\n"
]

for n, tt in zip(lista_n, TAU_A):
    tt = np.array(tt)
    txt_sem_filtragem_lines.append(f"=== Resultados para n = {n} ===\n")
    
    media = np.mean(tt)
    desvio = np.std(tt)
    cv = desvio / media

    relatorio = (
        f"  Sem eliminação de outliers (Dados Brutos):\n"
        f"    Elementos mantidos : {len(tt)} / {len(tt)}\n"
        f"    Média              : {media:.3e} s\n"
        f"    Desvio Padrão      : {desvio:.3e} s\n"
        f"    CV                 : {cv:.4f}\n"
        f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
    )
    txt_sem_filtragem_lines.append(relatorio)

    # Gráfico Histograma
    plt.figure()
    plt.hist(tt, bins=50, color='salmon', edgecolor='black')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Frequência")
    plt.title(f"Histograma Atribuição (Sem Filtragem) - n = {n}")
    plt.savefig(os.path.join(pasta_sem_filtragem, f"hist_n{n}.png"))
    plt.close()

    # Gráfico Curva de Tempo
    plt.figure()
    plt.plot(tt, marker='o', linestyle='-', color='crimson', markersize=3)
    plt.xlabel("Repetição")
    plt.ylabel("Tempo (s)")
    plt.title(f"Curva de Tempos Atribuição (Sem Filtragem) - n = {n}")
    plt.savefig(os.path.join(pasta_sem_filtragem, f"curva_n{n}.png"))
    plt.close()

with open(os.path.join(pasta_sem_filtragem, "resultados_sem_filtragem.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_sem_filtragem_lines)

# ==================== PROCESSAMENTO ATRIBUIÇÃO: MÉTODO 1 ====================
txt_metodo1_lines = metadados_hdr + [
    "========================================\n",
    "  RELATÓRIO DE RESULTADOS ATRIBUIÇÃO: MÉTODO 1 (DESVIO PADRÃO)\n",
    "========================================\n\n"
]

for n, tt in zip(lista_n, TAU_A):
    tt = np.array(tt)
    txt_metodo1_lines.append(f"=== Resultados para n = {n} ===\n")
    
    for x in [2, 3]:
        tt_filtrado = eliminar_outliers_desvio(tt, x=x)
        media = np.mean(tt_filtrado)
        desvio = np.std(tt_filtrado)
        cv = desvio / media

        relatorio = (
            f"  Filtro com x = {x} desvios padrão (Regra {x}σ):\n"
            f"    Elementos mantidos : {len(tt_filtrado)} / {len(tt)}\n"
            f"    Média              : {media:.3e} s\n"
            f"    Desvio Padrão      : {desvio:.3e} s\n"
            f"    CV                 : {cv:.4f}\n"
            f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
        )
        txt_metodo1_lines.append(relatorio)

        # Gráfico Histograma
        plt.figure()
        plt.hist(tt_filtrado, bins=50, color='skyblue', edgecolor='black')
        plt.xlabel("Tempo (s)")
        plt.ylabel("Frequência")
        plt.title(f"Histograma Atribuição (Método 1: {x}σ) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo1, f"hist_n{n}_{x}sigma.png"))
        plt.close()

        # Gráfico Curva de Tempo
        plt.figure()
        plt.plot(tt_filtrado, marker='o', linestyle='-', color='purple', markersize=3)
        plt.xlabel("Repetição (Filtrada)")
        plt.ylabel("Tempo (s)")
        plt.title(f"Curva de Tempos Atribuição (Método 1: {x}σ) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo1, f"curva_n{n}_{x}sigma.png"))
        plt.close()

with open(os.path.join(pasta_metodo1, "resultados_metodo1.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_metodo1_lines)

# ==================== PROCESSAMENTO ATRIBUIÇÃO: MÉTODO 2 ====================
txt_metodo2_lines = metadados_hdr + [
    "========================================\n",
    "  RELATÓRIO DE RESULTADOS ATRIBUIÇÃO: MÉTODO 2 (CORTE PERCENTUAL)\n",
    "========================================\n\n"
]

for n, tt in zip(lista_n, TAU_A):
    tt = np.array(tt)
    txt_metodo2_lines.append(f"=== Resultados para n = {n} ===\n")
    
    for pct in [0.02, 0.05]:
        pct_int = int(pct * 100)
        tt_filtrado = eliminar_outliers_corte_percentual(tt, pct=pct)
        media = np.mean(tt_filtrado)
        desvio = np.std(tt_filtrado)
        cv = desvio / media

        relatorio = (
            f"  Filtro cortando {pct_int}% do início e final:\n"
            f"    Elementos mantidos : {len(tt_filtrado)} / {len(tt)}\n"
            f"    Média              : {media:.3e} s\n"
            f"    Desvio Padrão      : {desvio:.3e} s\n"
            f"    CV                 : {cv:.4f}\n"
            f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
        )
        txt_metodo2_lines.append(relatorio)

        # Gráfico Histograma
        plt.figure()
        plt.hist(tt_filtrado, bins=50, color='lightgreen', edgecolor='black')
        plt.xlabel("Tempo (s)")
        plt.ylabel("Frequência")
        plt.title(f"Histograma Atribuição (Método 2: {pct_int}%) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo2, f"hist_n{n}_{pct_int}pct.png"))
        plt.close()

        # Gráfico Curva de Tempo
        plt.figure()
        plt.plot(tt_filtrado, marker='o', linestyle='-', color='orange', markersize=3)
        plt.xlabel("Repetição (Filtrada)")
        plt.ylabel("Tempo (s)")
        plt.title(f"Curva de Tempos Atribuição (Método 2: {pct_int}%) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo2, f"curva_n{n}_{pct_int}pct.png"))
        plt.close()

with open(os.path.join(pasta_metodo2, "resultados_metodo2.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_metodo2_lines)

# ==================== PROCESSAMENTO OPERAÇÃO (TAU_O): SEM FILTRAGEM ====================
txt_op_sem_filtragem_lines = metadados_hdr + [
    "========================================\n",
    "  RELATÓRIO DE RESULTADOS OPERAÇÃO (a + b): SEM FILTRAGEM (DADOS BRUTOS)\n",
    "========================================\n\n"
]

for n, tt_bruto, tt_iso in zip(lista_n, TAU_O_BRUTO, TAU_O_ISOLADO):
    tt_bruto = np.array(tt_bruto)
    tt_iso = np.array(tt_iso)
    txt_op_sem_filtragem_lines.append(f"=== Resultados Operação para n = {n} ===\n")
    
    # Primitiva Isolada (tau_o)
    media_iso = np.mean(tt_iso)
    desvio_iso = np.std(tt_iso)
    cv_iso = desvio_iso / media_iso if media_iso > 0 else 0

    # Tempo Total (x = a + b)
    media_bruto = np.mean(tt_bruto)
    desvio_bruto = np.std(tt_bruto)

    relatorio = (
        f"  Sem eliminação de outliers (Dados Brutos):\n"
        f"    Elementos mantidos        : {len(tt_iso)} / {len(tt_iso)}\n"
        f"    Tempo Total (x = a + b)   : {media_bruto:.3e} s (std: {desvio_bruto:.3e} s)\n"
        f"    Primitiva tau_o Isolada   : {media_iso:.3e} s\n"
        f"    Desvio Padrão (tau_o)     : {desvio_iso:.3e} s\n"
        f"    CV (tau_o)                : {cv_iso:.4f}\n"
        f"    CV < 0.15 ?               : {cv_iso < 0.15}\n\n"
    )
    txt_op_sem_filtragem_lines.append(relatorio)

    # Gráfico Histograma (tau_o Isolada)
    plt.figure()
    plt.hist(tt_iso, bins=50, color='teal', edgecolor='black')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Frequência")
    plt.title(f"Histograma Operação tau_o (Sem Filtragem) - n = {n}")
    plt.savefig(os.path.join(pasta_op_sem_filtragem, f"hist_n{n}.png"))
    plt.close()

    # Gráfico Curva de Tempo (tau_o Isolada)
    plt.figure()
    plt.plot(tt_iso, marker='o', linestyle='-', color='darkcyan', markersize=3)
    plt.xlabel("Repetição")
    plt.ylabel("Tempo (s)")
    plt.title(f"Curva de Tempos Operação tau_o (Sem Filtragem) - n = {n}")
    plt.savefig(os.path.join(pasta_op_sem_filtragem, f"curva_n{n}.png"))
    plt.close()

with open(os.path.join(pasta_op_sem_filtragem, "resultados_operacao_sem_filtragem.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_op_sem_filtragem_lines)

# ==================== PROCESSAMENTO OPERAÇÃO (TAU_O): MÉTODO 1 ====================
txt_op_metodo1_lines = metadados_hdr + [
    "========================================\n",
    "  RELATÓRIO DE RESULTADOS OPERAÇÃO (a + b): MÉTODO 1 (DESVIO PADRÃO)\n",
    "========================================\n\n"
]

for n, tt_iso in zip(lista_n, TAU_O_ISOLADO):
    tt_iso = np.array(tt_iso)
    txt_op_metodo1_lines.append(f"=== Resultados Operação para n = {n} ===\n")
    
    for x in [2, 3]:
        tt_filtrado = eliminar_outliers_desvio(tt_iso, x=x)
        media = np.mean(tt_filtrado)
        desvio = np.std(tt_filtrado)
        cv = desvio / media if media > 0 else 0

        relatorio = (
            f"  Filtro com x = {x} desvios padrão (Regra {x}σ):\n"
            f"    Elementos mantidos : {len(tt_filtrado)} / {len(tt_iso)}\n"
            f"    Média (tau_o)      : {media:.3e} s\n"
            f"    Desvio Padrão      : {desvio:.3e} s\n"
            f"    CV                 : {cv:.4f}\n"
            f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
        )
        txt_op_metodo1_lines.append(relatorio)

        # Gráfico Histograma
        plt.figure()
        plt.hist(tt_filtrado, bins=50, color='dodgerblue', edgecolor='black')
        plt.xlabel("Tempo (s)")
        plt.ylabel("Frequência")
        plt.title(f"Histograma Operação tau_o (Método 1: {x}σ) - n = {n}")
        plt.savefig(os.path.join(pasta_op_metodo1, f"hist_n{n}_{x}sigma.png"))
        plt.close()

        # Gráfico Curva de Tempo
        plt.figure()
        plt.plot(tt_filtrado, marker='o', linestyle='-', color='indigo', markersize=3)
        plt.xlabel("Repetição (Filtrada)")
        plt.ylabel("Tempo (s)")
        plt.title(f"Curva de Tempos Operação tau_o (Método 1: {x}σ) - n = {n}")
        plt.savefig(os.path.join(pasta_op_metodo1, f"curva_n{n}_{x}sigma.png"))
        plt.close()

with open(os.path.join(pasta_op_metodo1, "resultados_operacao_metodo1.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_op_metodo1_lines)

# ==================== PROCESSAMENTO OPERAÇÃO (TAU_O): MÉTODO 2 ====================
txt_op_metodo2_lines = metadados_hdr + [
    "========================================\n",
    "  RELATÓRIO DE RESULTADOS OPERAÇÃO (a + b): MÉTODO 2 (CORTE PERCENTUAL)\n",
    "========================================\n\n"
]

for n, tt_iso in zip(lista_n, TAU_O_ISOLADO):
    tt_iso = np.array(tt_iso)
    txt_op_metodo2_lines.append(f"=== Resultados Operação para n = {n} ===\n")
    
    for pct in [0.02, 0.05]:
        pct_int = int(pct * 100)
        tt_filtrado = eliminar_outliers_corte_percentual(tt_iso, pct=pct)
        media = np.mean(tt_filtrado)
        desvio = np.std(tt_filtrado)
        cv = desvio / media if media > 0 else 0

        relatorio = (
            f"  Filtro cortando {pct_int}% do início e final:\n"
            f"    Elementos mantidos : {len(tt_filtrado)} / {len(tt_iso)}\n"
            f"    Média (tau_o)      : {media:.3e} s\n"
            f"    Desvio Padrão      : {desvio:.3e} s\n"
            f"    CV                 : {cv:.4f}\n"
            f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
        )
        txt_op_metodo2_lines.append(relatorio)

        # Gráfico Histograma
        plt.figure()
        plt.hist(tt_filtrado, bins=50, color='mediumseagreen', edgecolor='black')
        plt.xlabel("Tempo (s)")
        plt.ylabel("Frequência")
        plt.title(f"Histograma Operação tau_o (Método 2: {pct_int}%) - n = {n}")
        plt.savefig(os.path.join(pasta_op_metodo2, f"hist_n{n}_{pct_int}pct.png"))
        plt.close()

        # Gráfico Curva de Tempo
        plt.figure()
        plt.plot(tt_filtrado, marker='o', linestyle='-', color='darkgreen', markersize=3)
        plt.xlabel("Repetição (Filtrada)")
        plt.ylabel("Tempo (s)")
        plt.title(f"Curva de Tempos Operação tau_o (Método 2: {pct_int}%) - n = {n}")
        plt.savefig(os.path.join(pasta_op_metodo2, f"curva_n{n}_{pct_int}pct.png"))
        plt.close()

with open(os.path.join(pasta_op_metodo2, "resultados_operacao_metodo2.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_op_metodo2_lines)

print("Execução concluída com sucesso!")
print(f"Resultados e gráficos de Atribuição salvos em '{pasta_sem_filtragem}', '{pasta_metodo1}' e '{pasta_metodo2}'.")
print(f"Resultados e gráficos de Operação salvos em '{pasta_op_sem_filtragem}', '{pasta_op_metodo1}' e '{pasta_op_metodo2}'.")

