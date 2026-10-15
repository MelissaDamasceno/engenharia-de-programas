from os import sched_get_priority_max
from datetime import MAXYEAR
import time

import matplotlib.pyplot as plt
import numpy as np
import cv2


# PRINTA DE IMAGEM ORIGINAL
# plt.imshow(img)
# plt.show()

def kmeans(img, K):
    
    n_linhas, n_colunas, c = img.shape

    ####### INICIALIZAÇÃO #######
    init = time.time()
    tic = time.time()

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


    init_time = time.time() - tic

    #### FIM DA INICIALIZAÇÃO ####


    MAX_ITER = 200
    iter = 0


    while True:
        CLUSTER = [[] for _ in range(K)]


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

        ###### FIM DO AGRUPAMENTO ######

        ########### CENTROIDE ##########
        tic = time.time()
        new_centroid = []
        for k in range(K):
            L = len(CLUSTER[k])
            if L == 0:  # cluster vazio: mantém o centroide anterior
                new_centroid.append(centroid[k])
                continue
            S = np.zeros(3)
            for px in CLUSTER[k]:
                S += [faixa[0][px], faixa[1][px], faixa[2][px]]    
            new_centroid.append([int(S[0])/L, int(S[1])/L, int(S[2])/L])

        centroid_time = time.time() - tic

        ##### FIM DO CENTROIDE #######

        ######## VERIFICAÇÃO #########

        conv = True 

        for k in range(K):
            for c in range(3):
                if int(centroid[k][c]) != int(new_centroid[k][c]):
                    conv = False
                    break

        ####### FIM DA VERIFICAÇÃO #########

        if not conv:
            centroid = new_centroid
            iter += 1

            if iter >= MAX_ITER:
                break

        else:
            break


    color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255]]

    segmented = np.empty((n_linhas, n_colunas, 3), dtype=np.uint8)

    for k in range(K):
        for px in CLUSTER[k]:
            i = px // n_colunas
            j = px % n_colunas
            segmented[i, j] = color[k]

    # plt.imshow(segmented)
    # plt.show()

    return segmented

if __name__ == '__main__':
    img = cv2.imread('imagem_original.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Formato jpg enxerga em BGR enquanto png, RGB
    kmeans(img, 2)
