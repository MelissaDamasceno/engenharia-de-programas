"""
Teste de equivalência: FCM Puro x FCM SoA (Missão 3 - Machado98).

Com a mesma semente aleatória, as duas variantes executam as mesmas
operações de ponto flutuante na mesma ordem. Portanto os centroides C,
a matriz U e a imagem segmentada devem ser IDÊNTICOS (igualdade exata).
Isso prova que a Missão 3 alterou apenas o layout da memória, não o algoritmo.

Uso: python teste_equivalencia.py
"""
import io
import os
import random
import contextlib
import importlib.util

import matplotlib
matplotlib.use("Agg")
from PIL import Image

PASTA = os.path.dirname(os.path.abspath(__file__))


def carrega_modulo(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(PASTA, arquivo))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def executa(modulo, img, K, semente):
    random.seed(semente)
    with contextlib.redirect_stdout(io.StringIO()):
        return modulo.fcm_processar_imagem(img, K, 2.0, 100, 0.01)


if __name__ == "__main__":
    puro = carrega_modulo("fcm_puro", "FCM_PURO_v3.py")
    soa = carrega_modulo("fcm_soa", "fcm_soa.py")

    caminho = os.path.join(PASTA, "..", "eng_prog", "imagens", "imagem_original.jpg")
    with Image.open(caminho) as original:
        img = original.convert("RGB").resize((60, 60))

    falhas = 0
    for K in (2, 3, 4):
        for semente in (0, 42):
            C_p, U_p, seg_p = executa(puro, img, K, semente)
            C_s, U_s, seg_s = executa(soa, img, K, semente)

            iguais = C_p == C_s and U_p == U_s and seg_p.tobytes() == seg_s.tobytes()
            print(f"K={K} semente={semente}: {'OK' if iguais else 'DIFERENTE'}")
            if not iguais:
                falhas += 1

    if falhas:
        raise SystemExit(f"\n[FALHA] {falhas} caso(s) divergiram entre Puro e SoA.")
    print("\n[SUCESSO] FCM SoA é idêntico ao FCM Puro em todos os casos.")
