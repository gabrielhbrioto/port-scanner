import socket
import re
import argparse

# Expressão Regular para endereços IPV4
ipv4_regex = r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'

def valid_ipv4(ip):
    return re.match(ipv4_regex, ip) is not None

class ServiceEntry:
    def __init__(self, name, port, protocol):
        self.name = name
        self.port = port
        self.protocol = protocol

    def __repr__(self):
        return f"Service(name='{self.name}', port={self.port}, protocol='{self.protocol}')"


def parse_services_file(file_path='/etc/services'):
    services = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Ignorar linhas vazias e comentários
            if not line or line.startswith('#'):
                continue

            # Quebrar a linha em seus componentes
            parts = line.split()

            # Nome do serviço é o primeiro campo
            name = parts[0]

            # Porta e protocolo são o segundo campo
            port_protocol = parts[1]
            port, protocol = port_protocol.split('/')

            # Criar um objeto ServiceEntry e adicionar à lista (sem alias)
            service = ServiceEntry(name=name, port=int(port), protocol=protocol)
            services.append(service)

    return services

def main():

    # Lendo e tratando o conteúdo do arquivo /etc/services
    services = parse_services_file()

    # Criação do parser de argumentos
    parser = argparse.ArgumentParser(description="Exemplo de programa com argumentos no formato p_start:p_stop ou apenas p_start")
    
    # Argumento para endereço de IP (obrigatório)
    parser.add_argument('ip', type=str, help="Endereço de IP (obrigatório)")
    
    # Definindo o argumento -p como opcional, permitindo que receba algo no formato p_start ou p_start:p_stop
    parser.add_argument('-p', type=str, nargs='?', help="Argumento no formato p_start ou p_start:p_stop", default='')

    # Parseando os argumentos
    args = parser.parse_args()

    # Validando o endereço de IP
    if(valid_ipv4(args.ip) is not True):
        print(f"The ip address {args.ip} is not a valid ip address")
        return
    
    # Parseando os argumentos
    ports = args.p

    # Verificando o valor passado para -p
    if ports:
        if ':' in ports:
            p_start_str, p_stop_str = ports.split(':')  # Dividindo p_start e p_stop pelo separador ":"
            p_start = int(p_start_str)
            p_stop = int(p_stop_str)
        else:
            p_start = int (ports)
            p_stop = 65535 # Atribuindo valor default ao segundo argumento
    else:
        p_start = 1 # Atribuindo valor default ao primeiro argumento
        p_stop = 65535 # Atribuindo valor default ao segundo argumento

    print(f"Port\tProtocol\tStatus")
    for port in range(p_start, p_stop+1):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        code = client.connect_ex((args.ip, port))
        if code == 0:
            for service in services:
                if(port == service.port):
                    print(f"{service.port}\t{service.protocol}\topen")

if __name__ == "__main__":
    main()