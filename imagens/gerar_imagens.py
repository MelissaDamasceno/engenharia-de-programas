"""
Gera os conjuntos de imagens dos experimentos a partir das 4 fotos de originais/.

- credito2/: cada foto em um tamanho irregular, de 35000 a 98000 pixels
  (bancada oficial do Crédito 2);
- escala_1x_4x/: n = 1x, 2x, 3x e 4x o da menor imagem (52x47 = 2444 pixels).

O conjunto escala_8pct/ (fotos a 8%, usado nos resultados do k-means) veio do
commit a8187c0 e está versionado como está; este script não o recria.

Uso: python imagens/gerar_imagens.py
"""
import os
from PIL import Image

PASTA = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(PASTA, "originais")

# (foto de origem, largura, altura): cada foto gera um n diferente
CREDITO2 = [
    ("WhatsApp Image 2026-10-13 at 08.36.16.jpeg", 175, 200),  # n = 35000
    ("imagem_original.jpg", 275, 225),                         # n = 61875
    ("WhatsApp Image 2026-10-13 at 08.36.14.jpeg", 310, 240),  # n = 74400
    ("WhatsApp Image 2026-10-13 at 08.36.15.jpeg", 350, 280),  # n = 98000
]

# Tamanhos com o aspecto da foto (erro < 2%) e n o mais perto possível do múltiplo
ESCALA_1X_4X = [
    ("WhatsApp Image 2026-10-13 at 08.36.15.jpeg", 52, 47),    # 1x: n = 2444
    ("WhatsApp Image 2026-10-13 at 08.36.16.jpeg", 81, 60),    # 2x: n = 4860
    ("imagem_original.jpg", 92, 80),                           # 3x: n = 7360
    ("WhatsApp Image 2026-10-13 at 08.36.14.jpeg", 163, 60),   # 4x: n = 9780
]


def redimensiona(foto, largura, altura):
    with Image.open(os.path.join(ORIGEM, foto)) as original:
        return original.convert("RGB").resize((largura, altura), Image.LANCZOS)


if __name__ == "__main__":
    destino = os.path.join(PASTA, "credito2")
    os.makedirs(destino, exist_ok=True)
    for foto, largura, altura in CREDITO2:
        nome_base = os.path.splitext(foto)[0].replace(" ", "_")
        caminho = os.path.join(destino, f"{nome_base}_{largura}x{altura}.png")
        redimensiona(foto, largura, altura).save(caminho)
        print(f"Gerada: {caminho} (n = {largura * altura})")

    destino = os.path.join(PASTA, "escala_1x_4x")
    os.makedirs(destino, exist_ok=True)
    for foto, largura, altura in ESCALA_1X_4X:
        caminho = os.path.join(destino, foto)
        redimensiona(foto, largura, altura).save(caminho, quality=95)
        print(f"Gerada: {caminho} (n = {largura * altura})")
