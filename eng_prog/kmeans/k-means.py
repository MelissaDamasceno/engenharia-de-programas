import time

import matplotlib.pyplot as plt
import numpy as np
import cv2


img = cv2.imread('massa.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Formato jpg enxerga em BGR enquanto png, RGB

n, m, c = img.shape
print(f'Número de Linhas: {n}\nNúmero de colunas: {m}\nNúmero de Cores: {c}')

# PRINTA DE IMAGEM ORIGINAL
# plt.imshow(img)
# plt.show()


####### INICIALIZAÇÃO #######
tic = time.time()

K = 2
faixa = []
plano = []
centroid = []

# Transforma a matrix de 3 dimensões em uma lista
for cor in range(c):
    plano.append(img[:,:,cor])

    # PLOTA IMAGEM EM CINZA DE CADA PLANO
    # plt.imshow(plano[-1], cmap='gray')
    # plt.show()

    faixa.append(plano[-1].flatten())

    # PRITA CADA FAIXA (R, G, B)
    # print(faixa)
    
    # PLOTA CADA FAIXA (R, G, B)
    # plt.scatter(np.arange(len(faixa[-1])), faixa[-1])
    # # plt.plot(faixa[-1])
    # plt.show()

# Escolhe aleatoriamente k centroides
n_pixels = len(faixa[0])
for k in range(K):
    px = np.random.randint(0, n_pixels)

    v = []
    for f in faixa:
        v.append(f[px])

    centroid.append(np.array(v))

    print(f'Centroid {k}: {centroid[-1]}')

init_time = time.time() - tic
print(f"Tempo de Inicialização: {init_time}")

#### FIM DA INICIALIZAÇÃO ####
        
MAX_ITER = 50
iter = 0
CLUSTER = [[] for _ in range(K)]
while True:
    ####### AGRUPAMENTO #########
    tic = time.time()

    for px in range(n_pixels):
        v = [faixa[0][px], faixa[1][px], faixa[2][px]]
        d = []
        for k in range(K):
            pxs_dist = np.linalg.norm(np.array(v) - np.array(centroid[k]))
            d.append(pxs_dist)
        cluster = np.argmin(d)
        CLUSTER[cluster].append(px)

        arrange_time = time.time() - tic        
    print(f"\n\nTamanho cluster 1: {len(CLUSTER[0])}\nTamanho cluster 2: {len(CLUSTER[1])}")
    print(f"Tempo de Agrupamento: {arrange_time}\n\n")
    ###### FIM DO AGRUPAMENTO ######
    
    ########### CENTROIDE ##########
    tic = time.time()
    new_centroid = []
    for k in range(K):
        L = len(CLUSTER[k])
        S = np.zeros(3)
        for px in CLUSTER[k]:
            S += [faixa[0][px], faixa[1][px], faixa[2][px]]    
        new_centroid.append([int(S[0])/L, int(S[1])/L, int(S[2])/L])
        print(f"Novo centroide {k}: {new_centroid[-1]}")

    centroid_time = time.time() - tic
    print(f"Tempo de Novo Centroide: {centroid_time}")
    ######## FIM DA CENTROIDE #######
    
    ########## VERIFICACAO #########
    conv = True
    for k in range(K):
        for c in range(3):
            if int(centroid[k][c]) != int(new_centroid[k][c]):
                conv = False
                break
    
    if not conv:
        centroid = new_centroid
        iter += 1
        print(f"Iteração: {iter}")
        if iter >= MAX_ITER:
            print(f"Não convergiu em {MAX_ITER} iterações")
            break
    else:
        print(f"Convergiu em {iter} iterações")
        break
    ###### FIM DA VERIFICACAO ######

            