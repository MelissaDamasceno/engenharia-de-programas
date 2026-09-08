import os
import platform
import multiprocessing

def obter_metadados_sistema():
    cpu_nome = platform.processor() or "Desconhecido"
    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        cpu_nome = line.split(":")[1].strip()
                        break
    except Exception:
        pass
    
    cores_logicos = multiprocessing.cpu_count()
    sys_info = f"{platform.system()} {platform.release()}"
    python_ver = platform.python_version()
    
    metadados = [
        "========================================\n",
        "  METADADOS E CONDIÇÕES DO EXPERIMENTO  \n",
        "========================================\n",
        f"  Processador          : {cpu_nome}\n",
        f"  Núcleos / Threads    : {cores_logicos}\n",
        f"  Memória RAM          : 16 GB\n",
        f"  Sistema Operacional  : Ubuntu 24.04.4 LTS ({sys_info})\n",
        f"  Versão do Python     : {python_ver}\n",
        f"  Fonte de Energia     : Conectado à Tomada (AC)\n",
        f"  Perfil de Energia    : Performance (Desempenho)\n",
        f"  Aplicações de Fundo  : Fechadas (Ambiente Limpo)\n",
        "========================================\n\n"
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
