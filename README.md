# Port Scanner

Este projeto é um scanner de portas TCP desenvolvido em Python, que permite escanear portas abertas em um endereço IP utilizando tanto IPv4 quanto IPv6, ou ainda um domínio. O script utiliza a biblioteca socket para realizar conexões TCP, identificando quais portas estão abertas em um determinado endereço.

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Dependências](#dependências)
- [Instalação](#instalação)
- [Execução](#execução)
- [Uso](#uso)
- [Licença](#licença)

## Descrição
Este é um simples scanner de portas desenvolvido em Python que permite verificar o status de portas em endereços IP IPv4 e IPv6. O script permite a verificação em redes locais ou remotas, identificando quais portas estão abertas para conexões TCP. Ele ainda oferece suporte DNS, permitindo ao usuário digitar o domínio que deseja escanear e resolvendo-o para um endereço de IP válido. Além disso, o projeto utiliza ambientes virtuais para a organização das dependências e fornece uma maneira de instalação global para facilitar sua execução.

## Funcionalidades
- Suporte a endereços IPv4 e IPv6.
- Suporte a DNS
- Validação de endereços IP.
- Verificação de portas abertas.
- Uso opcional de ambiente virtual para gerenciamento de dependências.
- Instalação simples do script no sistema com um link simbólico.

## Dependências
Certifique-se de ter as seguintes dependências instaladas:
- `Python v3.8.10` 
- `GCC v9.4.0` 
- `virtualenv v20.25.3` 
- `Ubuntu v20.04 LTS` 

## Instalação

### Passos para Instalar
1. Clone o repositório usando o comando `git clone` ou baixe os arquivos do projeto.
2. No diretório do projeto, execute o seguinte comando para instalar e configurar o ambiente virtual e o script:
    ```bash
    make install
    ```
    Esse comando criará um link simbólico em `/usr/local/bin/portscanner`, permitindo a execução do script em qualquer diretório do sistema com o comando `portscanner`.

## Execução

1. Executando o script instalado globalmente

Após concluída a instalação, você pode executar o scanner de portas com o seguinte comando:
```bash
portscanner <alvo>
```
Ou, se desejar, especificar o range de portas a serem scaneadas:

```bash
portscanner <alvo> -p <porta_inicial:porta_final>
```

2. Executando o script sem instalação prévia

Caso não seja do seu interesse criar o link simbólico para a execução do script, basta utilizar a diretiva `run` do `Makefile` fornecendo o ip da máquina alvo para escanear todas as portas:

```bash
make run ARGS="<alvo>"
```

Ou ainda para especificar o range de portas:

```bash
make run ARGS="<alvo> -p <porta_inicial:porta_final>"
```

3. Executando dentro do ambiente virtual

Para a execução dentro do ambiente virtual, primeiro é preciso verificar a existência ou não do ambiente virtual através do comando:

```bash
make venv_check
```

Caso o ambiente ainda não exista, ele pode ser criado através da diretiva `venv`:

```bash
make venv
```

Uma vez que o ambiente virtual já existe, basta seguir os passos apresentados na subseção anterior. Além disso, para remover o ambiente virtual, basta executar:

```bash
make clean
```

## Uso

O script requer um endereço IP como argumento que pode estar tanto no formato IPv4, quanto IPv6, além de aceitar como argumento um range de portas a serem escaneadas, ou apenas a porta inicial. Caso não sejam especificadas quais portas devem ser escaneadas, o algoritmo realizará o escaneamento da porta 1 à 65535.

Exemplo de execução utilizando como alvo a máquina metasploitable:

```bash
$ portscanner 192.168.1.4
Port            Status  Service
21\tcp          open    ftp
22\tcp          open    ssh
23\tcp          open    telnet
25\tcp          open    smtp
53\tcp          open    domain
80\tcp          open    http
111\tcp         open    sunrpc
139\tcp         open    netbios-ssn
445\tcp         open    microsoft-ds
512\tcp         open    exec
513\tcp         open    login
514\tcp         open    shell
1099\tcp        open    rmiregistry
1524\tcp        open    ingreslock
2049\tcp        open    nfs
2121\tcp        open    iprop
3306\tcp        open    mysql
3632\tcp        open    distcc
5432\tcp        open    postgresql
5900\tcp        open    unknown
6000\tcp        open    x11
6667\tcp        open    ircd
6697\tcp        open    ircs-u
8009\tcp        open    unknown
8180\tcp        open    unknown
8787\tcp        open    unknown
33291\tcp       open    unknown
34647\tcp       open    unknown
54968\tcp       open    unknown
55049\tcp       open    unknown
65535 ports scanned in 12.674 seconds
```

## Licença

Este projeto está licenciado sob a licença MIT.