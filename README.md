# Port Scanner

Este projeto é um scanner de portas TCP desenvolvido em Python, que permite escanear portas abertas em um endereço IP utilizando tanto IPv4 quanto IPv6. O script utiliza a biblioteca socket para realizar conexões TCP, identificando quais portas estão abertas em um determinado endereço.

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Dependências](#dependências)
- [Instalação](#instalação)
- [Execução](#execução)
- [Uso](#uso)
- [Licença](#licença)
## Descrição
Este é um simples scanner de portas desenvolvido em Python que permite verificar o status de portas em endereços IP IPv4 e IPv6. O script permite a verificação em redes locais ou remotas, identificando quais portas estão abertas para conexões TCP. Além disso, o projeto utiliza ambientes virtuais para a organização das dependências e fornece uma maneira de instalação global para facilitar sua execução.

## Funcionalidades
- Suporte a endereços IPv4 e IPv6.
- Validação de endereços IP.
- Verificação de portas abertas.
- Uso opcional de ambiente virtual para gerenciamento de dependências.
- Instalação fácil do script no sistema com um link simbólico.

## Dependências
Certifique-se de ter as seguintes dependências instaladas:
- Python 3.6 ou superior.
- `virtualenv` (gerenciamento de ambiente virtual).

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
portscanner <endereço IP>
```
Ou, se desejar, especificar o range de portas a serem scaneadas:

```bash
portscanner <endereço IP> -p <porta_inicial:porta_final>
```

2. Executando o script sem instalação prévia

Caso não seja do seu interesse criar o link simbólico para a execução do script, basta utilizar a diretiva `run` do `Makefile` fornecendo o ip da máquina alvo para escanear todas as portas:

```bash
make run ARGS="<endereço IP>"
```

Ou ainda para especificar o range de portas:

```bash
make run ARGS="<endereço IP> -p <porta_inicial:porta_final>"
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

Exemplo de execução:

```bash
$ portscanner 127.0.0.1
Port    Protocol        Status
80      tcp             open
5432    tcp             open
```

## Licença

Este projeto está licenciado sob a licença MIT.