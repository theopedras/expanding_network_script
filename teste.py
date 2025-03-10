import os
import subprocess
import time

def get_org_name(directory):
    spec_file = os.path.join(directory, "spec.yaml")
    if not os.path.exists(spec_file):
        raise FileNotFoundError(f"Arquivo spec.yaml não encontrado em {directory}")
    
    with open(spec_file, "r") as f:
        for line in f:
            if "peer1." in line:
                return line.strip().split(".")[1]  # Obtém "orgx" de "peer1.orgx.example.com"
    
    raise ValueError(f"Nome da organização não encontrado no spec.yaml de {directory}")

def join_network(base_dir, num_dirs):
    base_path = os.path.abspath(os.getcwd())  # Obtém o diretório atual absoluto
    main_site = os.path.join(base_path, f"{base_dir}0")  # Caminho absoluto para mysite0
    approved_sites = [main_site]  # Lista de diretórios já na rede

    if not os.path.exists(main_site):
        raise FileNotFoundError(f"Erro: Diretório {main_site} não encontrado. Execute o script na pasta correta.")

    print("Iniciando a rede Fabric existente...")
    # os.chdir(main_site)
    # subprocess.run(["./minifab", "up", "-e", "7000", "-n", "samplecc", "-p", ""], check=True)
    # time.sleep(10)
    # os.chdir(base_path)

    base_port = 7200  # Porta inicial para mysite1
    
    for i in range(1, num_dirs):
        new_site = os.path.join(base_path, f"{base_dir}{i}")  # Caminho absoluto para cada site
        if not os.path.exists(new_site):
            print(f"Erro: Diretório {new_site} não encontrado. Pulando...")
            continue

        org_name = get_org_name(new_site)
        port = base_port + (i - 1) * 100  # Incremento de 100 a cada iteração

        print(f"Iniciando a nova organização {new_site} na porta {port}...")
        os.chdir(new_site)
        subprocess.run(["./minifab", "netup", "-e", str(port), "-o", f"{org_name}.example.com"], check=True)
        time.sleep(10)
        os.chdir(base_path)

        print(f"Criando e copiando solicitação de ingresso para {new_site}...")
        join_request_src = os.path.join(new_site, "vars", f"JoinRequest_{org_name.replace('.', '-')}-example-com.json")
        join_request_dest = os.path.join(main_site, "vars", "NewOrgJoinRequest.json")

        print(f"Tentando copiar de: {join_request_src}")
        print(f"Para: {join_request_dest}")

        if not os.path.exists(join_request_src):
            print(f"Erro: Arquivo {join_request_src} não encontrado. Verificando diretório...")
            subprocess.run(["ls", "-l", os.path.join(new_site, "vars/")], check=True)
            return  # Sai da função para evitar erro

        subprocess.run(["cp", join_request_src, join_request_dest], check=True)
        os.chdir(main_site)
        subprocess.run(["./minifab", "orgjoin"], check=True)
        time.sleep(10)
        os.chdir(base_path)

        print(f"Importando nós de ordem e ingressando peers de {new_site} na rede...")
        os.chdir(new_site)
        subprocess.run(["cp", os.path.join(main_site, "vars", "profiles", "endpoints.yaml"), "vars"], check=True)
        subprocess.run(["./minifab", "nodeimport,join"], check=True)
        time.sleep(10)
        subprocess.run(["./minifab", "install,approve", "-n", "samplecc", "-p", ""], check=True)
        time.sleep(10)
        os.chdir(base_path)

        print(f"Aprovando {new_site} em todos os diretórios já na network...")
        for site in reversed(approved_sites):
            os.chdir(site)
            
            if site == main_site:
                print(f"Aprovando e commitando em {site} (mysite0)...")
                subprocess.run(["./minifab", "approve,discover,commit"], check=True)
            else:
                print(f"Aprovando em {site} sem commit...")
                subprocess.run(["./minifab", "approve,discover"], check=True)

            time.sleep(10)
            os.chdir(base_path)

        print(f"Descobrindo chaincode na nova organização {new_site}...")
        os.chdir(new_site)
        subprocess.run(["./minifab", "discover"], check=True)
        time.sleep(10)
        subprocess.run(["./minifab", "stats"], check=True)
        time.sleep(10)
        os.chdir(base_path)

        approved_sites.append(new_site)  # Adiciona o novo site à lista de aprovados

    print("Expansão da rede concluída com sucesso!")

if __name__ == "__main__":
    num_dirs = int(input("Digite o número de diretórios: "))
    join_network("mysite", num_dirs)
