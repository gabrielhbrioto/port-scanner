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
run: venv_check  ## Run the script inside the virtual environment, or globally if there is none
ifeq ($(venv_exists), 1)
	$(PYTHON) $(SCRIPT_NAME) $(ARGS)
else
	python3 $(SCRIPT_NAME) $(ARGS)
endif

# Instala as dependências no ambiente virtual ou globalmente
#setup: requirements.txt venv_check  ## Installs dependencies in the virtual or global environment
#ifeq ($(venv_exists), 1)
#	$(PIP) install -r requirements.txt
#else
#	pip install -r requirements.txt
#endif

# Remove arquivos gerados
clean:  ## Removes __pycache__ e venv
	rm -rf __pycache__
	rm -rf $(VENV_DIR)

# Cria o ambiente virtual
venv:  ## Creates the virtual environment if it does not exist
ifeq ($(venv_exists), 0)
	python3 -m venv $(VENV_DIR)
else
	@echo "Virtual environment already exists"
	@echo "Remove it with the clean directive before creating another one"
endif

# Verifica se o ambiente virtual existe
venv_check:  ## Checks if the virtual environment exists
ifeq ($(venv_exists), 1)
	@echo "Using the existing virtual environment"
else
	@echo "No virtual environment found"
	@echo "Using global system"
endif

# Diretiva de instalação: cria o link simbólico em /usr/local/bin
install:  ## Creates a symbolic link to run the script globally
	@if [ ! -f "$(SCRIPT_NAME)" ]; then \
		echo "Error: '$(SCRIPT_NAME)' script not found"; \
		exit 1; \
	fi
	@if [ -f "$(TARGET_PATH)" ]; then \
		echo "$(TARGET_NAME) is alredy installed in your system"; \
	else \
		chmod +x $(SCRIPT_NAME); \
		sudo ln -s $(CURDIR)/$(SCRIPT_NAME) $(TARGET_PATH); \
	fi

# Diretiva de desinstalação: remove o link simbólico de /usr/local/bin
uninstall:  ## Removes the symbolic link from system
	@if [ -f "$(TARGET_PATH)" ]; then \
		sudo rm $(TARGET_PATH); \
	fi
