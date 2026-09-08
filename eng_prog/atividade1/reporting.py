import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from filters import eliminar_outliers_desvio, eliminar_outliers_corte_percentual

def gerar_relatorios_atribuicao(TAU_A, lista_n, pasta_base, filtro_escolhido, metadados_hdr, x_escolhas=[2, 3], pct_escolhas=[0.02, 0.05]):
    """
    Gera relatórios de texto e gráficos para a medição de Atribuição (TAU_A).
    filtro_escolhido: '1' (sem filtro), '2' (desvio padrão), '3' (corte percentual), '4' (todos).
    """
    if filtro_escolhido in ['1', '4']:
        # Sem filtragem
        pasta_out = os.path.join(pasta_base, "sem_filtragem")
        os.makedirs(pasta_out, exist_ok=True)
        txt_lines = metadados_hdr + [
            "========================================\n",
            "  RELATÓRIO DE RESULTADOS ATRIBUIÇÃO: SEM FILTRAGEM (DADOS BRUTOS)\n",
            "========================================\n\n"
        ]
        for n, tt in zip(lista_n, TAU_A):
            tt = np.array(tt)
            txt_lines.append(f"=== Resultados para n = {n} ===\n")
            media = np.mean(tt)
            desvio = np.std(tt)
            cv = desvio / media if media > 0 else 0
            relatorio = (
                f"  Sem eliminação de outliers (Dados Brutos):\n"
                f"    Elementos mantidos : {len(tt)} / {len(tt)}\n"
                f"    Média              : {media:.3e} s\n"
                f"    Desvio Padrão      : {desvio:.3e} s\n"
                f"    CV                 : {cv:.4f}\n"
                f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
            )
            txt_lines.append(relatorio)
            
            plt.figure()
            plt.hist(tt, bins=50, color='salmon', edgecolor='black')
            plt.xlabel("Tempo (s)")
            plt.ylabel("Frequência")
            plt.title(f"Histograma Atribuição (Sem Filtragem) - n = {n}")
            plt.savefig(os.path.join(pasta_out, f"hist_n{n}.png"))
            plt.close()

            plt.figure()
            plt.plot(tt, marker='o', linestyle='-', color='crimson', markersize=3)
            plt.xlabel("Repetição")
            plt.ylabel("Tempo (s)")
            plt.title(f"Curva de Tempos Atribuição (Sem Filtragem) - n = {n}")
            plt.savefig(os.path.join(pasta_out, f"curva_n{n}.png"))
            plt.close()
            
        with open(os.path.join(pasta_out, "resultados_sem_filtragem.txt"), "w", encoding="utf-8") as f:
            f.writelines(txt_lines)

    if filtro_escolhido in ['2', '4']:
        # Método 1 (Desvio Padrão)
        pasta_out = os.path.join(pasta_base, "metodo1_desvio_padrao")
        os.makedirs(pasta_out, exist_ok=True)
        txt_lines = metadados_hdr + [
            "========================================\n",
            "  RELATÓRIO DE RESULTADOS ATRIBUIÇÃO: MÉTODO 1 (DESVIO PADRÃO)\n",
            "========================================\n\n"
        ]
        for n, tt in zip(lista_n, TAU_A):
            tt = np.array(tt)
            txt_lines.append(f"=== Resultados para n = {n} ===\n")
            for x in x_escolhas:
                tt_filtrado = eliminar_outliers_desvio(tt, x=x)
                media = np.mean(tt_filtrado)
                desvio = np.std(tt_filtrado)
                cv = desvio / media if media > 0 else 0
                relatorio = (
                    f"  Filtro com x = {x} desvios padrão (Regra {x}σ):\n"
                    f"    Elementos mantidos : {len(tt_filtrado)} / {len(tt)}\n"
                    f"    Média              : {media:.3e} s\n"
                    f"    Desvio Padrão      : {desvio:.3e} s\n"
                    f"    CV                 : {cv:.4f}\n"
                    f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
                )
                txt_lines.append(relatorio)

                plt.figure()
                plt.hist(tt_filtrado, bins=50, color='skyblue', edgecolor='black')
                plt.xlabel("Tempo (s)")
                plt.ylabel("Frequência")
                plt.title(f"Histograma Atribuição (Método 1: {x}σ) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"hist_n{n}_{x}sigma.png"))
                plt.close()

                plt.figure()
                plt.plot(tt_filtrado, marker='o', linestyle='-', color='purple', markersize=3)
                plt.xlabel("Repetição (Filtrada)")
                plt.ylabel("Tempo (s)")
                plt.title(f"Curva de Tempos Atribuição (Método 1: {x}σ) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"curva_n{n}_{x}sigma.png"))
                plt.close()
                
        with open(os.path.join(pasta_out, "resultados_metodo1.txt"), "w", encoding="utf-8") as f:
            f.writelines(txt_lines)

    if filtro_escolhido in ['3', '4']:
        # Método 2 (Corte Percentual)
        pasta_out = os.path.join(pasta_base, "metodo2_corte_percentual")
        os.makedirs(pasta_out, exist_ok=True)
        txt_lines = metadados_hdr + [
            "========================================\n",
            "  RELATÓRIO DE RESULTADOS ATRIBUIÇÃO: MÉTODO 2 (CORTE PERCENTUAL)\n",
            "========================================\n\n"
        ]
        for n, tt in zip(lista_n, TAU_A):
            tt = np.array(tt)
            txt_lines.append(f"=== Resultados para n = {n} ===\n")
            for pct in pct_escolhas:
                pct_int = int(pct * 100)
                tt_filtrado = eliminar_outliers_corte_percentual(tt, pct=pct)
                media = np.mean(tt_filtrado)
                desvio = np.std(tt_filtrado)
                cv = desvio / media if media > 0 else 0
                relatorio = (
                    f"  Filtro cortando {pct_int}% do início e final:\n"
                    f"    Elementos mantidos : {len(tt_filtrado)} / {len(tt)}\n"
                    f"    Média              : {media:.3e} s\n"
                    f"    Desvio Padrão      : {desvio:.3e} s\n"
                    f"    CV                 : {cv:.4f}\n"
                    f"    CV < 0.15 ?        : {cv < 0.15}\n\n"
                )
                txt_lines.append(relatorio)

                plt.figure()
                plt.hist(tt_filtrado, bins=50, color='lightgreen', edgecolor='black')
                plt.xlabel("Tempo (s)")
                plt.ylabel("Frequência")
                plt.title(f"Histograma Atribuição (Método 2: {pct_int}%) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"hist_n{n}_{pct_int}pct.png"))
                plt.close()

                plt.figure()
                plt.plot(tt_filtrado, marker='o', linestyle='-', color='orange', markersize=3)
                plt.xlabel("Repetição (Filtrada)")
                plt.ylabel("Tempo (s)")
                plt.title(f"Curva de Tempos Atribuição (Método 2: {pct_int}%) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"curva_n{n}_{pct_int}pct.png"))
                plt.close()
                
        with open(os.path.join(pasta_out, "resultados_metodo2.txt"), "w", encoding="utf-8") as f:
            f.writelines(txt_lines)

def gerar_relatorios_operacao(TAU_O_BRUTO, TAU_O_ISOLADO, lista_n, pasta_base, filtro_escolhido, metadados_hdr, x_escolhas=[2, 3], pct_escolhas=[0.02, 0.05]):
    """
    Gera relatórios de texto e gráficos para a medição de Operação (TAU_O).
    """
    if filtro_escolhido in ['1', '4']:
        pasta_out = os.path.join(pasta_base, "operacao_sem_filtragem")
        os.makedirs(pasta_out, exist_ok=True)
        txt_lines = metadados_hdr + [
            "========================================\n",
            "  RELATÓRIO DE RESULTADOS OPERAÇÃO (a + b): SEM FILTRAGEM (DADOS BRUTOS)\n",
            "========================================\n\n"
        ]
        for n, tt_bruto, tt_iso in zip(lista_n, TAU_O_BRUTO, TAU_O_ISOLADO):
            tt_bruto = np.array(tt_bruto)
            tt_iso = np.array(tt_iso)
            txt_lines.append(f"=== Resultados Operação para n = {n} ===\n")
            
            media_iso = np.mean(tt_iso)
            desvio_iso = np.std(tt_iso)
            cv_iso = desvio_iso / media_iso if media_iso > 0 else 0
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
            txt_lines.append(relatorio)

            plt.figure()
            plt.hist(tt_iso, bins=50, color='teal', edgecolor='black')
            plt.xlabel("Tempo (s)")
            plt.ylabel("Frequência")
            plt.title(f"Histograma Operação tau_o (Sem Filtragem) - n = {n}")
            plt.savefig(os.path.join(pasta_out, f"hist_n{n}.png"))
            plt.close()

            plt.figure()
            plt.plot(tt_iso, marker='o', linestyle='-', color='darkcyan', markersize=3)
            plt.xlabel("Repetição")
            plt.ylabel("Tempo (s)")
            plt.title(f"Curva de Tempos Operação tau_o (Sem Filtragem) - n = {n}")
            plt.savefig(os.path.join(pasta_out, f"curva_n{n}.png"))
            plt.close()
            
        with open(os.path.join(pasta_out, "resultados_operacao_sem_filtragem.txt"), "w", encoding="utf-8") as f:
            f.writelines(txt_lines)

    if filtro_escolhido in ['2', '4']:
        pasta_out = os.path.join(pasta_base, "operacao_metodo1_desvio_padrao")
        os.makedirs(pasta_out, exist_ok=True)
        txt_lines = metadados_hdr + [
            "========================================\n",
            "  RELATÓRIO DE RESULTADOS OPERAÇÃO (a + b): MÉTODO 1 (DESVIO PADRÃO)\n",
            "========================================\n\n"
        ]
        for n, tt_iso in zip(lista_n, TAU_O_ISOLADO):
            tt_iso = np.array(tt_iso)
            txt_lines.append(f"=== Resultados Operação para n = {n} ===\n")
            for x in x_escolhas:
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
                txt_lines.append(relatorio)

                plt.figure()
                plt.hist(tt_filtrado, bins=50, color='dodgerblue', edgecolor='black')
                plt.xlabel("Tempo (s)")
                plt.ylabel("Frequência")
                plt.title(f"Histograma Operação tau_o (Método 1: {x}σ) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"hist_n{n}_{x}sigma.png"))
                plt.close()

                plt.figure()
                plt.plot(tt_filtrado, marker='o', linestyle='-', color='indigo', markersize=3)
                plt.xlabel("Repetição (Filtrada)")
                plt.ylabel("Tempo (s)")
                plt.title(f"Curva de Tempos Operação tau_o (Método 1: {x}σ) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"curva_n{n}_{x}sigma.png"))
                plt.close()
                
        with open(os.path.join(pasta_out, "resultados_operacao_metodo1.txt"), "w", encoding="utf-8") as f:
            f.writelines(txt_lines)

    if filtro_escolhido in ['3', '4']:
        pasta_out = os.path.join(pasta_base, "operacao_metodo2_corte_percentual")
        os.makedirs(pasta_out, exist_ok=True)
        txt_lines = metadados_hdr + [
            "========================================\n",
            "  RELATÓRIO DE RESULTADOS OPERAÇÃO (a + b): MÉTODO 2 (CORTE PERCENTUAL)\n",
            "========================================\n\n"
        ]
        for n, tt_iso in zip(lista_n, TAU_O_ISOLADO):
            tt_iso = np.array(tt_iso)
            txt_lines.append(f"=== Resultados Operação para n = {n} ===\n")
            for pct in pct_escolhas:
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
                txt_lines.append(relatorio)

                plt.figure()
                plt.hist(tt_filtrado, bins=50, color='mediumseagreen', edgecolor='black')
                plt.xlabel("Tempo (s)")
                plt.ylabel("Frequência")
                plt.title(f"Histograma Operação tau_o (Método 2: {pct_int}%) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"hist_n{n}_{pct_int}pct.png"))
                plt.close()

                plt.figure()
                plt.plot(tt_filtrado, marker='o', linestyle='-', color='darkgreen', markersize=3)
                plt.xlabel("Repetição (Filtrada)")
                plt.ylabel("Tempo (s)")
                plt.title(f"Curva de Tempos Operação tau_o (Método 2: {pct_int}%) - n = {n}")
                plt.savefig(os.path.join(pasta_out, f"curva_n{n}_{pct_int}pct.png"))
                plt.close()
                
        with open(os.path.join(pasta_out, "resultados_operacao_metodo2.txt"), "w", encoding="utf-8") as f:
            f.writelines(txt_lines)
