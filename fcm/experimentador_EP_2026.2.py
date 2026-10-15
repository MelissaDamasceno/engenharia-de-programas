import os
import io
import re
import time
import random
import argparse
import contextlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # bancada sem janelas: os gráficos vão direto para arquivo
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit
import importlib.util

# ==========================================
# 0. Parâmetros da Bancada (Equipe 9 - Machado98, Missão 3 SoA)
# ==========================================
# Uso:
#   python experimentador_EP_2026.2.py --variante puro
#   python experimentador_EP_2026.2.py --variante soa
PASTA = os.path.dirname(os.path.abspath(__file__))
VARIANTES = {"puro": "FCM_PURO_v3.py", "soa": "fcm_soa.py"}

parser = argparse.ArgumentParser(description="Bancada F.O.C.A. do FCM (Puro x SoA)")
parser.add_argument("--variante", choices=VARIANTES.keys(), default="soa")
parser.add_argument("--repeticoes", type=int, default=30, help="R: repetições por (n, K)")
# epsilon = 0 nunca é atingido: toda execução faz exatamente max_iter iterações.
# Assim fotos e K diferentes não mudam o número de iterações e T(n, K) fica limpo.
parser.add_argument("--epsilon", type=float, default=0.0)
parser.add_argument("--max-iter", type=int, default=20)
parser.add_argument("--semente", type=int, default=42,
                    help="Semente fixa antes de cada repetição (mesma inicialização de U)")
parser.add_argument("--saida", default=os.path.join(PASTA, "resultados"))
args = parser.parse_args()

pasta_saida = os.path.join(args.saida, args.variante)
os.makedirs(pasta_saida, exist_ok=True)

# Carrega a variante do FCM pelo caminho do arquivo
_spec = importlib.util.spec_from_file_location(
    "fcm_" + args.variante, os.path.join(PASTA, VARIANTES[args.variante]))
fcm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fcm)

# ==========================================
# 1. Função do Aluno
# ==========================================
def segmenta_imagem(imagem, k):
    """
    Executa o FCM da variante escolhida sobre a imagem (PIL, RGB) já em memória.
    Retorna a imagem segmentada e o número de iterações executadas.
    """
    saida_fcm = io.StringIO()
    with contextlib.redirect_stdout(saida_fcm):
        _, _, imagem_segmentada = fcm.fcm_processar_imagem(
            img=imagem, K=k, m=2.0, max_iter=args.max_iter, epsilon=args.epsilon)

    # O FCM imprime "-> Convergiu na iteração X!" (X começa em 0)
    convergiu = re.search(r"iteração (\d+)", saida_fcm.getvalue())
    iteracoes = int(convergiu.group(1)) + 1 if convergiu else args.max_iter
    return imagem_segmentada, iteracoes

# ==========================================
# 2. Descoberta e Ordenação Ligeira (Sem estourar RAM)
# ==========================================
img_dir = os.path.join(PASTA, "imagens_fcm")  # gerada por gerar_imagens.py
k_list = [2, 3, 4]
R = args.repeticoes # Número de repetições por combinação

print(f"Variante: {args.variante} ({VARIANTES[args.variante]}) | R={R} | "
      f"epsilon={args.epsilon} | max_iter={args.max_iter} | semente={args.semente}")
print("Mapeando imagens e calculando 'n' (apenas cabeçalhos)...")
arquivos_n = []

# Varre os arquivos no diretório especificado
if os.path.exists(img_dir):
    for filename in os.listdir(img_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif')):
            filepath = os.path.join(img_dir, filename)

            # Image.open lê apenas os metadados. Não aloca a matriz de pixels.
            with Image.open(filepath) as img:
                w, h = img.size
                n = w * h
                arquivos_n.append({'arquivo': filename, 'caminho': filepath, 'n': n})

# Ordena a lista de dicionários pelo valor de 'n' crescente
arquivos_n = sorted(arquivos_n, key=lambda x: x['n'])

print(f"{len(arquivos_n)} imagens ordenadas prontas para processamento.")

# ==========================================
# 3. Execução (Carregando sob demanda)
# ==========================================
resultados = []

for item in arquivos_n:
    n = item['n']
    filepath = item['caminho']
    nome_arquivo = item['arquivo']

    print(f"Carregando {nome_arquivo} para a RAM (n={n})...")

    # Carrega a imagem real para a RAM apenas no momento de usar
    # (a conversão fica fora do cronômetro)
    with Image.open(filepath) as img:
        imagem = img.convert('RGB')

    # Executa todas as repetições e Ks para esta imagem
    for k in k_list:
        for r in range(R):
            # Mesma inicialização aleatória de U em todas as repetições,
            # para que o número de iterações não infle o CV
            random.seed(args.semente)

            t0 = time.perf_counter()
            seg_imagem, iteracoes = segmenta_imagem(imagem, k)
            t1 = time.perf_counter()
            print(f"  k={k} repetição {r + 1}/{R}: {t1 - t0:.4f}s ({iteracoes} iterações)", flush=True)

            if r == 0:
                nome_base = os.path.splitext(nome_arquivo)[0]
                seg_imagem.save(os.path.join(pasta_saida, f"segmentada_{nome_base}_k{k}.png"))

            resultados.append({
                'variante': args.variante,
                'arquivo': nome_arquivo,
                'n': n,
                'k': k,
                'repeticao': r,
                'tempo': (t1 - t0),
                'iteracoes': iteracoes
            })

    # Libera a RAM explicitamente antes de carregar a próxima imagem
    del imagem
    print(f"Análise de {nome_arquivo} concluída. Memória liberada.")

# Transforma os resultados em DataFrame
df_raw = pd.DataFrame(resultados)

# ==========================================
# 4. Pré-processamento e Validação F.O.C.A.
# ==========================================
if not df_raw.empty:
    # Guarda as medições brutas (todas as repetições) para auditoria
    df_raw.to_csv(os.path.join(pasta_saida, 'dados_brutos.csv'),
                  index=False, float_format='%.6f', sep=';', decimal=',')

    df_filtered = pd.DataFrame()

    # Filtragem de Outliers (Percentis 5 e 95)
    for (n, k), group in df_raw.groupby(['n', 'k']):
        p05 = group['tempo'].quantile(0.05)
        p95 = group['tempo'].quantile(0.95)
        valid_mask = (group['tempo'] >= p05) & (group['tempo'] <= p95)
        df_filtered = pd.concat([df_filtered, group[valid_mask]])

    # Validação de Estabilidade (Média, Desvio e CV)
    resumo = df_filtered.groupby(['n', 'k']).agg(
        tempo_medio=('tempo', 'mean'),
        desvio=('tempo', 'std'),
        contagem_valida=('tempo', 'count'),
        iteracoes_min=('iteracoes', 'min'),
        iteracoes_max=('iteracoes', 'max')
    ).reset_index()

    resumo['CV'] = resumo['desvio'] / resumo['tempo_medio']
    resumo['estavel_CV_menor_15'] = resumo['CV'] < 0.15

    pd.set_option('display.width', 200)
    print("\n--- Resumo de Estabilidade ---")
    print(resumo)

    def exibir_equacao_ajustada(popt, X_data, y_data):
        """
        Exibe no terminal a equação ajustada com notação científica legível,
        os coeficientes individuais e o coeficiente de determinação (R²).
        Retorna o R².
        """
        alpha, beta, gamma, delta = popt

        # Cálculo do R² (Coeficiente de Determinação)
        y_pred = model_n_k(X_data, *popt)
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

        print("\n" + "="*60)
        print(f"   MODELO EMPÍRICO AJUSTADO: T(n, K) - variante {args.variante}")
        print("="*60)
        print("Formulação Geral:")
        print("  T(n, K) = α·(n·K) + β·n + γ·K + δ\n")
        print("Parâmetros Identificados:")
        print(f"  α (alpha) = {alpha:14.6e} s/(pixel·cluster)")
        print(f"  β (beta)  = {beta:14.6e} s/pixel")
        print(f"  γ (gamma) = {gamma:14.6e} s/cluster")
        print(f"  δ (delta) = {delta:14.6e} s (overhead base)")
        print("-" * 60)
        print("Equação Parametrizada:")
        print(f"  T(n, K) = ({alpha:.4e})·(n·K) + ({beta:.4e})·n + ({gamma:.4e})·K + ({delta:.4e})")
        print(f"Aderência Estatística (R²): {r2:.4f}")
        print("="*60 + "\n")
        return r2

    # ==========================================
    # 5. Ajuste de Curvas
    # ==========================================
    def model_n_k(X, alpha, beta, gamma, delta):
        n, k = X
        return alpha * (n * k) + beta * n + gamma * k + delta

    X_data = np.vstack((resumo['n'], resumo['k']))
    y_data = resumo['tempo_medio']

    # O p0 pode precisar de sintonia dependendo da escala de tempo real
    # O ajuste precisa de mais pontos (n, k) que parâmetros (4) e de mais de um n
    popt = None
    if len(resumo) > 4 and resumo['n'].nunique() > 1:
        popt, _ = curve_fit(model_n_k, X_data, y_data, p0=[1e-6, 1e-6, 1e-6, 0.01], maxfev=10000)
        resumo['tempo_predito'] = model_n_k(X_data, *popt)
        r2 = exibir_equacao_ajustada(popt, X_data, y_data)

        # Coeficientes em arquivo próprio, para comparar Puro x SoA
        pd.DataFrame([{
            'variante': args.variante, 'alpha': popt[0], 'beta': popt[1],
            'gamma': popt[2], 'delta': popt[3], 'R2': r2
        }]).to_csv(os.path.join(pasta_saida, 'coeficientes.csv'),
                   index=False, float_format='%.6e', sep=';', decimal=',')
    else:
        print("Poucos pontos para o ajuste de curva; pulando.")
        resumo['tempo_predito'] = np.nan

    # ==========================================
    # 6. Plotagens Bidimensionais
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot A: Tempo vs n
    colors_k = ['red', 'green', 'blue', 'orange', 'purple']
    for idx, k in enumerate(k_list):
        dados_k = resumo[resumo['k'] == k]
        if not dados_k.empty:
            c = colors_k[idx % len(colors_k)]
            ax1.plot(dados_k['n'], dados_k['tempo_medio'], marker='o',
                     color=c, label=f'K={k} (Empírico)')
            ax1.plot(dados_k['n'], dados_k['tempo_predito'], linestyle='--',
                     color=c, alpha=0.6)

    ax1.set_xlabel('Número de Pixels (n)')
    ax1.set_ylabel('Tempo Médio de Execução (s)')
    ax1.set_title('Tempo vs Tamanho da Imagem')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot B: Tempo vs K
    n_processados = sorted(resumo['n'].unique())
    colors_n = plt.cm.viridis(np.linspace(0, 1, len(n_processados)))

    for idx, n_val in enumerate(n_processados):
        dados_n = resumo[resumo['n'] == n_val]
        if not dados_n.empty:
            ax2.plot(dados_n['k'], dados_n['tempo_medio'], marker='s',
                     color=colors_n[idx], label=f'n={n_val}')
            ax2.plot(dados_n['k'], dados_n['tempo_predito'], linestyle='--',
                     color=colors_n[idx], alpha=0.6)

    ax2.set_xlabel('Número de Clusters (K)')
    ax2.set_title('Tempo vs Número de Clusters')
    ax2.set_xticks(k_list)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, 'relatorio_complexidade.png'), dpi=300)
    plt.close(fig)

    print(f"\nGráficos 2D salvos em '{pasta_saida}/relatorio_complexidade.png'.")

    # ==========================================
    # 6b. Superfície 3D (Figura 2 do relatório)
    # ==========================================
    if popt is not None:
        n_grade, k_grade = np.meshgrid(
            np.linspace(resumo['n'].min(), resumo['n'].max(), 40),
            np.linspace(min(k_list), max(k_list), 40))
        t_grade = model_n_k((n_grade, k_grade), *popt)

        fig = plt.figure(figsize=(9, 7))
        ax3 = fig.add_subplot(projection='3d')
        ax3.plot_surface(n_grade, k_grade, t_grade, cmap='viridis', alpha=0.55)
        ax3.scatter(resumo['n'], resumo['k'], resumo['tempo_medio'],
                    color='red', s=30, depthshade=False, label='Medições (média)')
        ax3.set_xlabel('Número de Pixels (n)')
        ax3.set_ylabel('Número de Clusters (K)')
        ax3.set_zlabel('Tempo (s)')
        ax3.set_yticks(k_list)
        ax3.set_title(f'Superfície T(n, K) ajustada - FCM {args.variante}')
        ax3.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(pasta_saida, 'superficie_3d_foca.png'), dpi=300)
        plt.close(fig)
        print(f"Superfície 3D salva em '{pasta_saida}/superficie_3d_foca.png'.")

    # ==========================================
    # 7. Exportação dos Dados para Avaliação
    # ==========================================
    arquivo_csv = os.path.join(pasta_saida, 'resultados_foca_aluno.csv')

    # Exporta os dados usando ponto e vírgula como separador e vírgula para decimais,
    # garantindo que o arquivo seja aberto corretamente no Excel em PT-BR.
    resumo.to_csv(arquivo_csv, index=False, float_format='%.6f', sep=';', decimal=',')

    print(f"Tabela de avaliação exportada com sucesso para: {arquivo_csv}")

else:
    print("\nNenhum dado processado. Verifique se o diretório contém imagens válidas.")
