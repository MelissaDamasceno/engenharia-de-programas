import numpy as np

# Método 1: Eliminar outliers usando a regra de x desvios padrão (x = 2 ou x = 3)
def eliminar_outliers_desvio(tt, x=3):
    tt = np.asarray(tt)
    media_bruta = np.mean(tt)
    desvio_bruto = np.std(tt)
    limite_inferior = media_bruta - x * desvio_bruto
    limite_superior = media_bruta + x * desvio_bruto
    return tt[(tt >= limite_inferior) & (tt <= limite_superior)]

def filtrar_outliers_desvio_detalhado(tt, x=3):
    """
    Aplica a regra dos x desvios padrão retornando:
    inliers, mascara_inliers, limite_inferior, limite_superior, media_bruta, desvio_bruto
    """
    tt = np.asarray(tt)
    media_bruta = np.mean(tt)
    desvio_bruto = np.std(tt)
    lim_inf = media_bruta - x * desvio_bruto
    lim_sup = media_bruta + x * desvio_bruto
    mascara_inliers = (tt >= lim_inf) & (tt <= lim_sup)
    return tt[mascara_inliers], mascara_inliers, lim_inf, lim_sup, media_bruta, desvio_bruto

# Método 2: Eliminar outliers cortando p% das extremidades (menores e maiores valores)
def eliminar_outliers_corte_percentual(tt, pct=0.02):
    tt_ordenado = np.sort(np.asarray(tt))
    n_corte = int(len(tt_ordenado) * pct)
    if n_corte == 0:
        return tt_ordenado
    return tt_ordenado[n_corte:-n_corte]

