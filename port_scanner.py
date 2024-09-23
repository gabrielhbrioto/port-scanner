#!/usr/bin/env python3

import socket
import re
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

socket_type = None
ip_address = None
services = []

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
    global services

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

def scan_port(port):
    client = socket.socket(socket_type, socket.SOCK_STREAM)
    client.settimeout(0.1)
    code = client.connect_ex((ip_address, port))
    if code == 0:
        for service_index, service in enumerate(services):
            if port == service.port:
                return f"{service.port}\{service.protocol}\t\topen\t{service.name}"
        return f"{port}\{service.protocol}\topen\tunknown"
    return None

def dns_lookup(hostname):
    try:
        # Para IPv4 e IPv6
        addr_info = socket.getaddrinfo(hostname, None)
        # Filtra os endereços IPv4 e IPv6
        ipv4_address = None
        ipv6_address = None
        for info in addr_info:
            family, _, _, _, sockaddr = info
            if family == socket.AF_INET:  # IPv4
                ipv4_address = sockaddr[0]
            elif family == socket.AF_INET6:  # IPv6
                ipv6_address = sockaddr[0]
        
        return ipv4_address, ipv6_address
    except socket.gaierror:
        return None, None

def main():
    global socket_type
    global ip_address

    # Lendo e tratando o conteúdo do arquivo /etc/services
    services = parse_services_file()

    # Criação do parser de argumentos
    parser = argparse.ArgumentParser(description="Script for port scanning")
    
    # Argumento para endereço de IP (obrigatório)
    parser.add_argument('target', type=str, help="IP Address or hostname")
    
    # Definindo o argumento -p como opcional, permitindo que receba algo no formato p_start ou p_start:p_stop
    parser.add_argument('-p', type=str, nargs='?', help="Port range <p_start:p_stop> <p_start> [default: 1:65535]", default='1:65535')

    # Flag opcional --parallelize para ativar o escaneamento em paralelo
    parser.add_argument('--parallelize', action='store_true', help="Enable parallel scanning")
    
    # Parseando os argumentos
    args = parser.parse_args()

    # Resolvendo o hostname para IPv4 e IPv6, se for um domínio
    ipv4_address, ipv6_address = dns_lookup(args.target)

    # Validando o endereço de IP
    if valid_ipv4(args.target) or ipv4_address:
        socket_type = socket.AF_INET
        ip_address = ipv4_address if ipv4_address else args.target
    elif valid_ipv6(args.target) or ipv6_address:
        socket_type = socket.AF_INET6
        ip_address = ipv6_address if ipv6_address else args.target
    else:
        print(f"\033[31mError:\033[0m Failed to resolve \"{args.target}\"")
        return

    # Parseando as portas
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

    # Salvando instante inicial do escaneamento de portas
    init_time = time.time()

    # Impressão do cabeçalho da saída
    print(f"Port\t\tStatus\tService")

    # Escaneamento paralelo
    if args.parallelize:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(scan_port, port) for port in range(p_start, p_stop+1)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(result)
    
    # Loop de escaneamento sequencial
    else:
        for port in range(p_start, p_stop+1):
                result = scan_port(port)
                if result:
                    print(result)
    
    print(f"{p_stop-p_start+1} ports scanned in {(time.time()-init_time):.3f} seconds")
                
if __name__ == "__main__":
    main()