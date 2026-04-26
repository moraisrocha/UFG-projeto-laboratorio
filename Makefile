# Variáveis para facilitar a manutenção
PYTHON = python3
PIP = pip
APP_MODULE = app.main
TEST_DIR = app/tests

.PHONY: install run test lint clean help

help:
	@echo "Comandos disponíveis:"
	@echo "  make install  - Instala as dependências listadas em requirements.txt"
	@echo "  make run      - Inicia o servidor FastAPI (app.main)"
	@echo "  make test     - Executa todos os testes unitários e de integração"
	@echo "  make lint     - Formata o código fonte utilizando o Black"
	@echo "  make clean    - Remove arquivos temporários e caches de execução"

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m $(APP_MODULE)

test:
	$(PYTHON) -m pytest -v $(TEST_DIR)

lint:
	$(PYTHON) -m black .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +