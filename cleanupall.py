import os
import subprocess

def get_org_name(directory):
    """Obtém o nome da organização a partir do spec.yaml."""
    spec_file = os.path.join(directory, "spec.yaml")
    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Arquivo spec.yaml não encontrado em {directory}")
    
    with open(spec_file, "r") as f:
        for line in f:
            if "peer1." in line:
                return line.strip().split(".")[1]  # Obtém "orgX" de "peer1.orgX.example.com"
    
    raise ValueError(f"Nome da organização não encontrado no spec.yaml de {directory}")

def cleanup_mysites(base_dir, num_dirs):
    """Executa o minifab cleanup em cada mysiteX com a flag -o da organização correspondente."""
    base_path = os.path.abspath(os.getcwd())  # Obtém o diretório absoluto do script
    print(f"Iniciando cleanup em {num_dirs} sites...")

    for i in range(num_dirs):
        site_path = os.path.join(base_path, f"{base_dir}{i}")  # Caminho absoluto para cada site
        
        if os.path.exists(site_path):
            try:
                org_name = get_org_name(site_path)  # Obtém o nome da organização
                print(f"Limpando {site_path} para a organização {org_name}...")
                os.chdir(site_path)
                subprocess.run(["./minifab", "cleanup", "-o", f"{org_name}.example.com"], check=True)
            except Exception as e:
                print(f"Erro ao processar {site_path}: {e}")
        else:
            print(f"Diretório {site_path} não encontrado. Pulando...")

    print("Cleanup concluído!")

if __name__ == "__main__":
    num_dirs = int(input("Digite o número total de mysites: "))
    cleanup_mysites("mysite", num_dirs)
