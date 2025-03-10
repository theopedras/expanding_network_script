import os
import subprocess

def create_directories_and_run_script(num_dirs):
    for i in range(1, num_dirs + 1):
        dir_name = f"mysite{i-1}"
        os.makedirs(dir_name, exist_ok=True)
        
        # Baixar o script minifab dentro do diretório
        minifab_path = os.path.join(dir_name, "minifab")
        subprocess.run(["curl", "-o", minifab_path, "-sL", "https://tinyurl.com/yxa2q6yr"], check=True)
        
        # Tornar o script minifab executável
        subprocess.run(["chmod", "+x", minifab_path], check=True)
        
        # Executar o script scriptspec.py na raiz
        subprocess.run(["python3", "scriptspec.py"], check=True)
        
        # Mover o arquivo gerado para dentro do diretório
        spec_file_path = "spec.yaml"
        if os.path.exists(spec_file_path):
            subprocess.run(["mv", spec_file_path, dir_name], check=True)

if __name__ == "__main__":
    num_dirs = int(input("Digite o número de diretórios: "))

    create_directories_and_run_script(num_dirs)
