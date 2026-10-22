# Engenharia de Programas 2026.2 · Equipe 9 Machado98

Bruno Novais, Caio Lucena e Melissa Damasceno. UNEB, Prof. Dr. Diego Frias Suarez.

| Pasta | O que tem |
| --- | --- |
| [`calibracao_foca/`](calibracao_foca/) | Crédito 1: validação do setup (RTA) e calibração das primitivas F.O.C.A. (τ_a, τ_c, τ_o) |
| [`kmeans/`](kmeans/) | Nosso k-means em Python puro (`k-means.py`) e saídas de exemplo |
| [`fcm/`](fcm/) | Crédito 2: FCM Puro × FCM SoA (Missão 3), bancada oficial e relatório |
| [`experimentador/`](experimentador/) | Experimentador da disciplina, único para todos os algoritmos, e os resultados de cada rodada |
| [`imagens/`](imagens/) | Fotos originais e os conjuntos de imagens gerados a partir delas |
| [`material/`](material/) | PDFs e modelos fornecidos pelo professor |

## Ambiente

Um único venv na raiz, com o Python 3.10.12 do sistema (o mesmo da calibração F.O.C.A.):

```bash
/usr/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Rodar o experimentador

Da raiz, com o notebook na tomada e preso a um P-core (no i7-13620H, as CPUs 0–11 são P-cores e as 12–15 são E-cores). Sem o `taskset`, o processo migra entre os núcleos e o tempo varia em blocos:

```bash
taskset -c 4 .venv/bin/python experimentador/experimentador.py --algoritmo fcm_puro --imagens escala_1x_4x
```

Detalhes e a lista de resultados em [`experimentador/README.md`](experimentador/README.md).
