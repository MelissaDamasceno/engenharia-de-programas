"""
Gera as imagens da bancada a partir das 4 fotos de eng_prog/imagens/,
cada uma redimensionada para um tamanho irregular (n = largura x altura distintos).

Uso: python gerar_imagens.py
"""
import os
from PIL import Image

PASTA = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(PASTA, "..", "eng_prog", "imagens")
DESTINO = os.path.join(PASTA, "imagens_fcm")

# (foto de origem, largura, altura): cada foto gera um n diferente
IMAGENS = [
    ("WhatsApp Image 2026-10-13 at 08.36.16.jpeg", 175, 200),  # n = 35000
    ("imagem_original.jpg", 275, 225),                         # n = 61875
    ("WhatsApp Image 2026-10-13 at 08.36.14.jpeg", 310, 240),  # n = 74400
    ("WhatsApp Image 2026-10-13 at 08.36.15.jpeg", 350, 280),  # n = 98000
]

if __name__ == "__main__":
    os.makedirs(DESTINO, exist_ok=True)

    for foto, largura, altura in IMAGENS:
        nome_base = os.path.splitext(foto)[0].replace(" ", "_")
        caminho = os.path.join(DESTINO, f"{nome_base}_{largura}x{altura}.png")

        with Image.open(os.path.join(ORIGEM, foto)) as original:
            original.convert("RGB").resize((largura, altura), Image.LANCZOS).save(caminho)
        print(f"Gerada: {caminho} (n = {largura * altura}, origem: {foto})")
