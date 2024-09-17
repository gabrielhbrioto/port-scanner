#!/usr/bin/env python3

import socket
import re
import argparse
import copy

# Expressão Regular para endereços IPV4
ipv4_regex = r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'
ipv6_regex = re.compile(
    r'('
    r'(([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:))|'
    r'(([0-9a-fA-F]{1,4}:){1,7}:)|'
    r'(([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4})|'
    r'(([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2})|'
    r'(([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3})|'
    r'(([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4})|'
    r'(([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5})|'
    r'([0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6}))|'
    r'(:(:[0-9a-fA-F]{1,4}){1,7}|:)|'
    r'fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|'
    r'::(ffff(:0{1,4}){0,1}:){0,1}'
    r'(([0-9]{1,3}\.){3}[0-9]{1,3})|'
    r'([0-9a-fA-F]{1,4}:){1,4}:([0-9]{1,3}\.){3}[0-9]{1,3}'
    r')'
)

# Funções de validação
def valid_ipv6(ip):
    if ipv6_regex.match(ip):
        return True
    return False

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
    parser = argparse.ArgumentParser(description="Script for port scanning")
    
    # Argumento para endereço de IP (obrigatório)
    parser.add_argument('ip', type=str, help="IP Address")
    
    # Definindo o argumento -p como opcional, permitindo que receba algo no formato p_start ou p_start:p_stop
    parser.add_argument('-p', type=str, nargs='?', help=" port range <p_start:p_stop> <p_start> [default: 1:65535]", default='1:65535')

    # Parseando os argumentos
    args = parser.parse_args()

    # Validando o endereço de IP
    if(valid_ipv4(args.ip) is not True and valid_ipv6(args.ip) is not True):
        print(f"The ip address {args.ip} is not a valid ip address")
        return
    elif(valid_ipv4(args.ip)):
        socket_type = socket.AF_INET
    else:
        socket_type = socket.AF_INET6

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

    print(f"Port\tProtocol\tStatus\tService")
    for port in range(p_start, p_stop+1):
        client = socket.socket(socket_type, socket.SOCK_STREAM)
        client.settimeout(0.1)
        code = client.connect_ex((args.ip, port))
        if code == 0:
            for service_index, service in enumerate(services):
                if(port == service.port):
                    print(f"{service.port}\t{service.protocol}\t\topen\t{service.name}")
                    break
                if(service_index == len(services)): # Se service_index == len(services) -> True é porque se trata da última iteração e o serviço n foi encontrao
                    print(f"{service.port}\t{service.protocol}\t\topen\tunknown")

                    
                
if __name__ == "__main__":
    main()