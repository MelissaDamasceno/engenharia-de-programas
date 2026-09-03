import os
import sys
from utils import obter_metadados_sistema
from experiment import run_assignment_experiment, run_operation_experiment, run_comparison_experiment
from reporting import gerar_relatorios_atribuicao, gerar_relatorios_operacao, gerar_relatorios_comparacao

def main():
    print("=========================================")
    print("       EXPERIMENTOS DE DESEMPENHO        ")
    print("=========================================")
    print("Escolha o experimento a ser executado:")
    print("  1 - Atribuição (tau_a)")
    print("  2 - Operação (tau_o)")
    print("  3 - Comparação (tau_c): variável vs constante")
    print("  4 - Todos")
    exp_escolha = input("Digite o número (1/2/3/4) [padrão: 4]: ").strip()
    if not exp_escolha:
        exp_escolha = '4'
        
    print("\nEscolha o método de filtragem de outliers:")
    print("  1 - Sem filtragem (Dados Brutos)")
    print("  2 - Método 1 (Desvio Padrão)")
    print("  3 - Método 2 (Corte Percentual)")
    print("  4 - Todos os métodos")
    filtro_escolha = input("Digite o número (1/2/3/4) [padrão: 4]: ").strip()
    if not filtro_escolha:
        filtro_escolha = '4'
        
    x_escolhas = [2, 3]
    if filtro_escolha in ['2', '4']:
        print("\nPara o Método 1 (Desvio Padrão), escolha o valor de x:")
        print("  1 - x = 2")
        print("  2 - x = 3")
        print("  3 - Ambos (2 e 3)")
        x_opt = input("Digite o número (1/2/3) [padrão: 3]: ").strip()
        if x_opt == '1': x_escolhas = [2]
        elif x_opt == '2': x_escolhas = [3]
        
    pct_escolhas = [0.02, 0.05]
    if filtro_escolha in ['3', '4']:
        print("\nPara o Método 2 (Corte Percentual), escolha a porcentagem:")
        print("  1 - 2%")
        print("  2 - 5%")
        print("  3 - Ambos (2% e 5%)")
        pct_opt = input("Digite o número (1/2/3) [padrão: 3]: ").strip()
        if pct_opt == '1': pct_escolhas = [0.02]
        elif pct_opt == '2': pct_escolhas = [0.05]
        
    pasta_base = input("\nDigite o nome da pasta para salvar os resultados [padrão: resultados]: ").strip()
    if not pasta_base:
        pasta_base = "resultados"
        
    os.makedirs(pasta_base, exist_ok=True)
    
    lista_n = [1000, 10000, 100000]
    R = 100
    metadados_hdr = obter_metadados_sistema()
    
    TAU_A = None
    if exp_escolha in ['1', '4']:
        TAU_A = run_assignment_experiment(lista_n, R)
        gerar_relatorios_atribuicao(TAU_A, lista_n, pasta_base, filtro_escolha, metadados_hdr, x_escolhas, pct_escolhas)
        
    if exp_escolha in ['2', '3', '4'] and TAU_A is None:
        # Precisa rodar atribuição para subtrair a baseline, mas não precisa gerar relatório
        TAU_A = run_assignment_experiment(lista_n, R)
        
    if exp_escolha in ['2', '4']:
        TAU_O_BRUTO, TAU_O_ISOLADO = run_operation_experiment(lista_n, R, TAU_A)
        gerar_relatorios_operacao(TAU_O_BRUTO, TAU_O_ISOLADO, lista_n, pasta_base, filtro_escolha, metadados_hdr, x_escolhas, pct_escolhas)
        
    if exp_escolha in ['3', '4']:
        TAU_C_VAR_BRUTO, TAU_C_VAR_ISOLADO, TAU_C_CONST_BRUTO, TAU_C_CONST_ISOLADO = run_comparison_experiment(lista_n, R, TAU_A)
        gerar_relatorios_comparacao(TAU_C_VAR_BRUTO, TAU_C_VAR_ISOLADO, lista_n, pasta_base, filtro_escolha, metadados_hdr, x_escolhas, pct_escolhas, rotulo="a < b", prefixo="comparacao_variavel")
        gerar_relatorios_comparacao(TAU_C_CONST_BRUTO, TAU_C_CONST_ISOLADO, lista_n, pasta_base, filtro_escolha, metadados_hdr, x_escolhas, pct_escolhas, rotulo="a < CONSTANTE", prefixo="comparacao_constante")
        
    print(f"\nExecução concluída com sucesso! Resultados salvos na pasta '{pasta_base}'.")

if __name__ == "__main__":
    main()
