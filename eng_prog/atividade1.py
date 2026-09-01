import os
from time import time
import matplotlib
matplotlib.use('Agg')  # Para evitar que janelas interativas travem a geração de gráficos
from matplotlib import pyplot as plt
import numpy as np

# Configuração das pastas de saída
pasta_sem_filtragem = "sem_filtragem"
pasta_metodo1 = "metodo1_desvio_padrao"
pasta_metodo2 = "metodo2_corte_percentual"

os.makedirs(pasta_sem_filtragem, exist_ok=True)
os.makedirs(pasta_metodo1, exist_ok=True)
os.makedirs(pasta_metodo2, exist_ok=True)

lista_n = [1000, 10000, 100000]
R = 100
t = []

# Medição dos tempos
print("Coletando medições de tempo...")
for n in lista_n:
    tt = []
    for r in range(R):
        tic = time()
        for i in range(n):
            x = 1
        toc = time()
        tt.append(toc - tic)
    t.append(tt)

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

# ==================== PROCESSAMENTO SEM FILTRAGEM ====================
txt_sem_filtragem_lines = ["========================================\n",
                           "  RELATÓRIO DE RESULTADOS: SEM FILTRAGEM (DADOS BRUTOS)\n",
                           "========================================\n\n"]

for n, tt in zip(lista_n, t):
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
    plt.title(f"Histograma (Sem Filtragem) - n = {n}")
    plt.savefig(os.path.join(pasta_sem_filtragem, f"hist_n{n}.png"))
    plt.close()

    # Gráfico Curva de Tempo
    plt.figure()
    plt.plot(tt, marker='o', linestyle='-', color='crimson', markersize=3)
    plt.xlabel("Repetição")
    plt.ylabel("Tempo (s)")
    plt.title(f"Curva de Tempos (Sem Filtragem) - n = {n}")
    plt.savefig(os.path.join(pasta_sem_filtragem, f"curva_n{n}.png"))
    plt.close()

with open(os.path.join(pasta_sem_filtragem, "resultados_sem_filtragem.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_sem_filtragem_lines)

# ==================== PROCESSAMENTO MÉTODO 1 ====================
txt_metodo1_lines = ["========================================\n",
                     "  RELATÓRIO DE RESULTADOS: MÉTODO 1 (DESVIO PADRÃO)\n",
                     "========================================\n\n"]

for n, tt in zip(lista_n, t):
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
        plt.title(f"Histograma (Método 1: {x}σ) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo1, f"hist_n{n}_{x}sigma.png"))
        plt.close()

        # Gráfico Curva de Tempo
        plt.figure()
        plt.plot(tt_filtrado, marker='o', linestyle='-', color='purple', markersize=3)
        plt.xlabel("Repetição (Filtrada)")
        plt.ylabel("Tempo (s)")
        plt.title(f"Curva de Tempos (Método 1: {x}σ) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo1, f"curva_n{n}_{x}sigma.png"))
        plt.close()

with open(os.path.join(pasta_metodo1, "resultados_metodo1.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_metodo1_lines)

# ==================== PROCESSAMENTO MÉTODO 2 ====================
txt_metodo2_lines = ["========================================\n",
                     "  RELATÓRIO DE RESULTADOS: MÉTODO 2 (CORTE PERCENTUAL)\n",
                     "========================================\n\n"]

for n, tt in zip(lista_n, t):
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
        plt.title(f"Histograma (Método 2: {pct_int}%) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo2, f"hist_n{n}_{pct_int}pct.png"))
        plt.close()

        # Gráfico Curva de Tempo
        plt.figure()
        plt.plot(tt_filtrado, marker='o', linestyle='-', color='orange', markersize=3)
        plt.xlabel("Repetição (Filtrada)")
        plt.ylabel("Tempo (s)")
        plt.title(f"Curva de Tempos (Método 2: {pct_int}%) - n = {n}")
        plt.savefig(os.path.join(pasta_metodo2, f"curva_n{n}_{pct_int}pct.png"))
        plt.close()

with open(os.path.join(pasta_metodo2, "resultados_metodo2.txt"), "w", encoding="utf-8") as f:
    f.writelines(txt_metodo2_lines)

print("Execução concluída com sucesso!")
print(f"Resultados e gráficos salvos em '{pasta_sem_filtragem}', '{pasta_metodo1}' e '{pasta_metodo2}'.")
