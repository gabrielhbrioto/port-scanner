VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# Verifica se o ambiente virtual existe
venv_exists = $(shell [ -d $(VENV_DIR) ] && echo "1" || echo "0")

# Diretiva para exibir o help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

run: venv_check  ## Executa o script port_scanner.py dentro do ambiente virtual se existir, caso contrário, usa o Python global
ifeq ($(venv_exists), 1)
	$(PYTHON) port_scanner.py
else
	python port_scanner.py
endif

##setup: requirements.txt venv_check  ## Instala as dependências do requirements.txt no ambiente virtual ou global
##ifeq ($(venv_exists), 1)
##	$(PIP) install -r requirements.txt
##else
##	pip install -r requirements.txt
##endif

clean:  ## Remove o diretório venv e o cache __pycache__
	rm -rf __pycache__
	rm -rf $(VENV_DIR)

venv:  ## Cria o ambiente virtual se ele não existir
ifeq ($(venv_exists), 0)
	python3 -m venv $(VENV_DIR)
else
	@echo "Ambiente virtual já existente. Remova-o com a diretiva clean antes de criar outro."
endif

venv_check:  ## Verifica se o ambiente virtual existe e exibe uma mensagem correspondente
ifeq ($(venv_exists), 1)
	@echo "Usando o ambiente virtual existente."
else
	@echo "Nenhum ambiente virtual encontrado. Usando o sistema global."
endif
