# FCM · Missão 3 (Structure of Arrays) · Equipe 9 Machado98

| Arquivo | O que é |
| --- | --- |
| `FCM_PURO_v3.py` | Código base da disciplina, **sem alterações** (grupo controle) |
| `fcm_soa.py` | Nossa variante: pixels em `X_R`, `X_G`, `X_B` |
| `teste_equivalencia.py` | Prova que Puro e SoA dão C, U e imagem idênticos com a mesma semente |
| `gerar_imagens.py` | Gera `imagens_fcm/` com as fotos de `eng_prog/imagens/` em tamanhos irregulares (175×200 a 350×280) |
| `experimentador_EP_2026.2.py` | Cópia adaptada do experimentador da disciplina |

## Preparar o ambiente (uma vez)

Usar o Python 3.10.12 do sistema, o mesmo da calibração F.O.C.A.:

```bash
/usr/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python gerar_imagens.py
.venv/bin/python teste_equivalencia.py
```

## Rodar a bancada

Sempre na mesma máquina, na tomada e com os outros programas fechados:

```bash
.venv/bin/python experimentador_EP_2026.2.py --variante puro
.venv/bin/python experimentador_EP_2026.2.py --variante soa
```

Cada rodada grava em `resultados/<variante>/`:

- `dados_brutos.csv`: todas as repetições, com tempo e número de iterações
- `resultados_foca_aluno.csv`: média, desvio e CV por (n, K) (Tabela 1 do relatório)
- `coeficientes.csv`: α, β, γ, δ e R² do ajuste T(n, K)
- `relatorio_complexidade.png`: Figura 1 (T × n e T × K)
- `superficie_3d_foca.png`: Figura 2 (superfície ajustada com os pontos medidos)
- `segmentada_*.png`: a segmentação da primeira repetição de cada (n, K)

Opções: `--repeticoes` (padrão 30), `--epsilon` (0.0), `--max-iter` (20), `--semente` (42), `--saida` (`resultados`).

Com `epsilon = 0` o critério de convergência nunca é atingido, então toda execução faz exatamente `max-iter` iterações. Como as fotos são diferentes, isso impede que o número de iterações mude de uma imagem para outra e distorça T(n, K).

A semente é fixada antes de cada repetição para que a inicialização aleatória de U seja sempre a mesma. Sem isso, o número de iterações varia e o CV passa de 0,15.
