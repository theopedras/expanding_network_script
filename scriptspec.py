def generate_config_file(num_orderers, orgs, peers_per_org):
    orderer_list = [f"orderer{i}.example.com" for i in range(1, num_orderers + 1)]
    
    peer_list = []
    for org in orgs:
        for peer in range(1, peers_per_org + 1):
            peer_list.append(f"peer{peer}.{org}.example.com")
    
    config_data = f"""fabric:
  peers:
{create_yaml_list(peer_list)}
"""
    
    if num_orderers > 0:
        config_data += f"  orderers:\n{create_yaml_list(orderer_list)}\n"
    
    with open("spec.yaml", "w") as config_file:
        config_file.write(config_data)
    
    print("Arquivo spec.yaml gerado com sucesso!")

def create_yaml_list(items):
    return '\n'.join([f'  - "{item}"' for item in items])

if __name__ == "__main__":
    num_orderers = int(input("Digite o número de orderers: "))
    orgs = input("Digite os nomes das organizações separados por vírgula: ").split(',')
    peers_per_org = int(input("Digite o número de peers por organização: "))
    
    generate_config_file(num_orderers, orgs, peers_per_org)
