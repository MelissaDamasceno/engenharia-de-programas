from matplotlib import pyplot as plt
from time import time
import numpy as np

lista_n = [1000, 10000, 100000]
R = 100
t = []

for n in lista_n:
    tt = []
    for r in range(R):
        tic = time()
        for i in range(n):
            x = 1
        toc = time()
        tt.append(toc - tic)
    t.append(tt)
    plt.hist(tt, bins=50)
    plt.xlabel("tempo (s)")
    plt.title(f"n = {n}")
    plt.savefig(f"histn{n}.png")
    plt.show()


# plotar a curva
for n, tt in zip(lista_n, t):
    plt.figure()
    plt.plot(tt)
    plt.xlabel("repeticao")
    plt.ylabel("tempo (s)")
    plt.title(f"n = {n}")
    plt.savefig(f"curvan{n}.png")
    plt.show()

# para cada n
for n, tt in zip(lista_n, t):
    tt = np.array(tt)

    # determinar valor de corte: 10% acima do menor tempo medido
    valor_corte = 1.10 * tt.min()

    # filtrar
    tt_filtrado = tt[tt < valor_corte]

    # calcular
    media = np.mean(tt_filtrado)
    desvio = np.std(tt_filtrado)
    cv = desvio / media

    print(f"n = {n}")
    print(f"  valor de corte = {valor_corte:.3e} s")
    print(f"  media          = {media:.3e} s")
    print(f"  desvio         = {desvio:.3e} s")
    print(f"  cv             = {cv:.4f}")
    print(f"  cv < 0.15 ?      {cv < 0.15}")
