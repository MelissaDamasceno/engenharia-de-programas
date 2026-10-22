# Imagens

| Pasta | Conteúdo | n (pixels) |
| --- | --- | --- |
| `originais/` | As 4 fotos em resolução cheia, fonte de todos os outros conjuntos | 385 mil a 591 mil |
| `credito2/` | Bancada oficial do Crédito 2 (175×200 a 350×280) | 35000, 61875, 74400, 98000 |
| `escala_1x_4x/` | n = 1×, 2×, 3× e 4× o da menor imagem (52×47) | 2444, 4860, 7360, 9780 |
| `escala_8pct/` | Fotos a 8% da escala, usadas nos resultados do k-means | 2444, 3008, 3348, 3774 |

`credito2/` e `escala_1x_4x/` são recriadas a partir de `originais/` com o comando abaixo, e o resultado é idêntico aos arquivos versionados:

```bash
.venv/bin/python imagens/gerar_imagens.py
```

`escala_8pct/` foi gerada de outra forma (commit a8187c0) e está versionada como está.
