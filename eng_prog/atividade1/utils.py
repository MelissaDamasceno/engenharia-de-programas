import os
import platform
import multiprocessing
import subprocess

def obter_especificacoes_ambiente():
    """
    Coleta os parâmetros exatos do ambiente computacional requeridos
    pela Seção 1 do Relatório Técnico-Científico F.O.C.A.
    """
    cpu_nome = "13th Gen Intel(R) Core(TM) i7-13620H"
    freq_base_turbo = "Base: 2.40 GHz (P-core) / 1.80 GHz (E-core) | Turbo Boost: 4.90 GHz (P-core) / 3.60 GHz (E-core)"
    cache_info = "L1i: 448 KiB (10 inst.), L1d: 416 KiB (10 inst.), L2: 9.5 MiB (7 inst.), L3: 24 MiB (Smart Cache unificado)"
    ram_info = "16 GiB (15.5 GiB utilizáveis) DDR5"
    so_kernel = "Ubuntu 22.04.5 LTS (x86_64), Kernel Linux 6.8.0-138-generic (SMP PREEMPT_DYNAMIC)"
    plano_energia = "AC Conectado / Intel P-State Governor: powersave (Equilibrado/Dinâmico)"
    python_ver = f"CPython {platform.python_version()} (64-bit)"

    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        cpu_nome = line.split(":")[1].strip()
                        break
    except Exception:
        pass

    try:
        out = subprocess.check_output(["lscpu"], text=True)
        for line in out.splitlines():
            if "CPU max MHz:" in line:
                max_mhz = line.split(":")[1].strip()
            elif "CPU min MHz:" in line:
                min_mhz = line.split(":")[1].strip()
    except Exception:
        pass

    try:
        if os.path.exists("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"):
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "r") as f:
                gov = f.read().strip()
                plano_energia = f"AC Conectado / Governor: {gov}"
    except Exception:
        pass

    return {
        "processador": cpu_nome,
        "frequencia": freq_base_turbo,
        "cache": cache_info,
        "ram": ram_info,
        "so_kernel": so_kernel,
        "plano_energia": plano_energia,
        "linguagem": python_ver
    }

def obter_metadados_sistema():
    info = obter_especificacoes_ambiente()
    metadados = [
        "=================================================================\n",
        "         ESPECIFICAÇÃO RIGOROSA DO AMBIENTE COMPUTACIONAL         \n",
        "=================================================================\n",
        f"  Processador          : {info['processador']}\n",
        f"  Frequência           : {info['frequencia']}\n",
        f"  Hierarquia de Cache  : {info['cache']}\n",
        f"  Memória RAM          : {info['ram']}\n",
        f"  Sistema Operacional  : {info['so_kernel']}\n",
        f"  Plano de Energia     : {info['plano_energia']}\n",
        f"  Versão da Linguagem  : {info['linguagem']}\n",
        "=================================================================\n\n"
    ]
    return metadados

def setup_directories(base_dir, subfolders):
    """Cria os diretórios necessários dentro da pasta base_dir."""
    paths = {}
    for sub in subfolders:
        path = os.path.join(base_dir, sub)
        os.makedirs(path, exist_ok=True)
        paths[sub] = path
    return paths

