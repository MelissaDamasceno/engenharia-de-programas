# Experimentador F.O.C.A.

`experimentador.py` é o experimentador da disciplina adaptado para medir T(n, K) de qualquer um dos nossos algoritmos. Para cada imagem, cada K ∈ {2, 3, 4} e cada uma das R repetições, ele:

1. fixa a semente;
2. cronometra a segmentação;
3. filtra os outliers (P5 a P95);
4. calcula média, desvio e CV;
5. ajusta T(n, K) = α·n·K + β·n + γ·K + δ.

| Opção | Padrão | O que faz |
| --- | --- | --- |
| `--algoritmo` | `fcm_puro` | `kmeans`, `fcm_puro` ou `fcm_soa` |
| `--imagens` | `escala_1x_4x` | subpasta de `imagens/`: `escala_1x_4x`, `credito2` ou `escala_8pct` |
| `--repeticoes` | 30 | R, as repetições por (n, K) |
| `--epsilon`, `--max-iter` | 0.0, 20 | só para o FCM; com ε = 0, toda execução faz exatamente `max-iter` iterações |
| `--semente` | 42 | fixada antes de **cada** execução, em `random` (FCM) e em `np.random` (k-means) |
| `--sem-semente` | | não fixa a semente |
| `--saida` | `resultados/<algoritmo>_<imagens>` | pasta onde os resultados são gravados |

Cada rodada grava:
- `dados_brutos.csv`
- `resultados_foca_aluno.csv`
- `coeficientes.csv`
- `relatorio_complexidade.png` (T × n e T × K)
- `superficie_3d_foca.png`
- `segmentada_*.png`, a segmentação da primeira repetição de cada (n, K)

## Resultados

| Pasta | Algoritmo | Imagens | Condições | R² |
| --- | --- | --- | --- | --- |
| `resultados/kmeans_seed_igual/` | k-means | `escala_8pct` | `np.random.seed(0)` antes de cada execução | 0,57 |
| `resultados/kmeans_seed_diferente/` | k-means | `escala_8pct` | sem semente | 0,81 |
| `resultados/fcm_puro_1x_4x/` | FCM Puro | `escala_1x_4x` | ε = 0, 20 iterações, semente 42, `taskset -c 4`, na bateria | 0,9986 |

As pastas do k-means e do FCM Puro foram geradas pelo experimentador que ficava em `eng_prog/` (histórico do git). Por isso só têm o resumo, o gráfico 2D e a saída do terminal (`terminal.txt`).

Para reproduzir os resultados do k-means com o script atual:

```bash
.venv/bin/python experimentador/experimentador.py --algoritmo kmeans --imagens escala_8pct --semente 0
```

O k-means converge num número de passadas que varia com a foto e com K. Com a semente fixa, cada par (n, K) fica com uma contagem arbitrária, e por isso o ajuste de T(n, K) sai fraco. No FCM, ε = 0 fixa o número de iterações e o ajuste fica limpo.

A bancada oficial do Crédito 2 (FCM Puro × SoA, imagens `credito2`) fica em [`../fcm/resultados/`](../fcm/resultados/).
