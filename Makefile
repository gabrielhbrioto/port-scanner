VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip
SCRIPT_NAME=port_scanner.py
TARGET_NAME=portscanner
TARGET_PATH=/usr/local/bin/$(TARGET_NAME)

# Verifica se o ambiente virtual existe
venv_exists = $(shell [ -d $(VENV_DIR) ] && echo "1" || echo "0")

# Diretiva para exibir o help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Executa o script dentro ou fora do ambiente virtual
run: venv_check  ## Executa o script dentro do ambiente virtual, ou globalmente se não houver
ifeq ($(venv_exists), 1)
	$(PYTHON) $(SCRIPT_NAME)
else
	python $(SCRIPT_NAME)
endif

# Instala as dependências no ambiente virtual ou globalmente
#setup: requirements.txt venv_check  ## Instala dependências no ambiente virtual ou global
#ifeq ($(venv_exists), 1)
#	$(PIP) install -r requirements.txt
#else
#	pip install -r requirements.txt
#endif

# Remove arquivos gerados
clean:  ## Remove __pycache__ e venv
	rm -rf __pycache__
	rm -rf $(VENV_DIR)

# Cria o ambiente virtual
venv:  ## Cria o ambiente virtual se ele não existir
ifeq ($(venv_exists), 0)
	python3 -m venv $(VENV_DIR)
else
	@echo "Ambiente virtual já existente. Remova-o com a diretiva clean antes de criar outro."
endif

# Verifica se o ambiente virtual existe
venv_check:  ## Verifica se o ambiente virtual existe
ifeq ($(venv_exists), 1)
	@echo "Usando o ambiente virtual existente."
else
	@echo "Nenhum ambiente virtual encontrado. Usando o sistema global."
endif

# Diretiva de instalação: cria o link simbólico em /usr/local/bin
install:  ## Cria um link simbólico para executar o script globalmente
	@if [ ! -f "$(SCRIPT_NAME)" ]; then \
		echo "Erro: O script '$(SCRIPT_NAME)' não foi encontrado."; \
		exit 1; \
	fi
	@if [ -f "$(TARGET_PATH)" ]; then \
		echo "$(TARGET_NAME) is alredy installed in your system"; \
	else \
		chmod +x $(SCRIPT_NAME); \
		sudo ln -s $(CURDIR)/$(SCRIPT_NAME) $(TARGET_PATH); \
	fi

# Diretiva de desinstalação: remove o link simbólico de /usr/local/bin
uninstall:  ## Remove o link simbólico do sistema
	@if [ -f "$(TARGET_PATH)" ]; then \
		sudo rm $(TARGET_PATH); \
	fi
