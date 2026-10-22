# FCM · Missão 3 (Structure of Arrays) · Equipe 9 Machado98

| Arquivo | O que é |
| --- | --- |
| `FCM_PURO_v3.py` | Código base da disciplina, **sem alterações** (grupo controle) |
| `fcm_soa.py` | Nossa variante: pixels em `X_R`, `X_G`, `X_B` |
| `teste_equivalencia.py` | Prova que Puro e SoA dão C, U e imagem idênticos com a mesma semente |
| `resultados/` | Bancada oficial (Puro e SoA), usada no relatório |
| `relatorio/` | Relatório do Crédito 2 (`main.tex` e `main.pdf`) |

O experimentador e o gerador de imagens ficam fora desta pasta, porque são compartilhados com as outras atividades: [`experimentador/`](../experimentador/) e [`imagens/`](../imagens/). As imagens desta bancada são as de `imagens/credito2/` (175×200 a 350×280).

## Preparar o ambiente (uma vez)

Da raiz do repositório, usar o Python 3.10.12 do sistema, o mesmo da calibração F.O.C.A.:

```bash
/usr/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python imagens/gerar_imagens.py
.venv/bin/python fcm/teste_equivalencia.py
```

## Rodar a bancada

Sempre na mesma máquina, na tomada e com os outros programas fechados. Os comandos abaixo, executados da raiz, reproduzem a bancada oficial:

```bash
.venv/bin/python experimentador/experimentador.py --algoritmo fcm_puro --imagens credito2 --saida fcm/resultados/puro
.venv/bin/python experimentador/experimentador.py --algoritmo fcm_soa  --imagens credito2 --saida fcm/resultados/soa
```

Cada rodada grava na pasta de `--saida`:

- `dados_brutos.csv`: todas as repetições, com tempo e número de iterações
- `resultados_foca_aluno.csv`: média, desvio e CV por (n, K) (Tabela 1 do relatório)
- `coeficientes.csv`: α, β, γ, δ e R² do ajuste T(n, K)
- `relatorio_complexidade.png`: Figura 1 (T × n e T × K)
- `superficie_3d_foca.png`: Figura 2 (superfície ajustada com os pontos medidos)
- `segmentada_*.png`: a segmentação da primeira repetição de cada (n, K)

Opções: `--repeticoes` (padrão 30), `--epsilon` (0.0), `--max-iter` (20), `--semente` (42). A bancada oficial foi rodada sem `taskset`, com o script que ficava nesta pasta (`experimentador_EP_2026.2.py`, no histórico do git). A única diferença do script atual é que a coluna `variante` dos CSVs passou a se chamar `algoritmo`.

Com `epsilon = 0` o critério de convergência nunca é atingido, então toda execução faz exatamente `max-iter` iterações. Como as fotos são diferentes, isso impede que o número de iterações mude de uma imagem para outra e distorça T(n, K).

A semente é fixada antes de cada repetição para que a inicialização aleatória de U seja sempre a mesma. Sem isso, o número de iterações varia e o CV passa de 0,15.
