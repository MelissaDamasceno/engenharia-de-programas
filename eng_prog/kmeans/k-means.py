import matplotlib.pyplot as plt
import numpy as np
import cv2


img = cv2.imread('massa.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Fromato jpg enxerga em BGR enquanto npg, RGB

n, m, c = img.shape
# print(f'linha: {n}, colunas: {m}, cores: {c}')


# plt.imshow(img)
# plt.show()

##### INICIALIZAÇÃO ####

K = 2
faixa = []
plano = []
centroid = []

# Transforma a matrix de 3 dimensões em uma lista
for cor in range(c):
    plano.append(img[:,:,cor])
    # plt.imshow(plano[-1], cmap='gray')
    # plt.show()
    faixa.append(plano[-1].flatten())
    # print(faixa)

    # plt.scatter(np.arange(len(faixa[-1])), faixa[-1])
    # # plt.plot(faixa[-1])
    # plt.show()


# Escolhe aleatoriamente k centroides
n_pixels = len(faixa[0])
for k in range(K):
    px = np.random.randint(0, n_pixels)
    # py = np.random.randint(0, n_pixels)
    # pz = np.random.randint(0, n_pixels)

    # v0 = faixa[0][px]
    # v1 = faixa[1][px]
    # v2 = faixa[2][px]

    # centroid.append([v0, v1, v2])

    v = []
    for f in faixa:
        v.append(f[px])

    centroid.append(np.array(v))

    print(centroid[-1])



#### FIM DA INICIALIZAÇÃO ####

####### AGRUPAMENTO #########

clusters = np.array((k, n_pixels), dtype='int')
n_px_clusters = []

for f in faixa:
    