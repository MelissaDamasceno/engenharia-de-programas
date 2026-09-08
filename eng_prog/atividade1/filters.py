import numpy as np

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
