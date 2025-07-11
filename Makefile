# Makefile para projeto Django com Conda e Git Bash

# Nome do ambiente Conda
ENV_NAME=newlife

# Caminho do requirements.txt
REQ=requirements.txt

# Nome do app principal Django (onde está o settings.py)
APP=setup

# Ativação do conda para Git Bash
CONDA_RUN=source ~/miniconda3/etc/profile.d/conda.sh && conda activate $(ENV_NAME)

.PHONY: help install run migrate makemigrations shell test clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make install          - Instala as dependências do projeto"
	@echo "  make run              - Inicia o servidor Django"
	@echo "  make migrate          - Aplica migrações"
	@echo "  make makemigrations   - Cria migrações para o app principal"
	@echo "  make shell            - Abre o shell do Django"
	@echo "  make test             - Executa os testes"
	@echo "  make clean            - Remove arquivos .pyc e __pycache__"

install:
	$(CONDA_RUN) && pip install -r $(REQ)

check:
	$(CONDA_RUN) && python manage.py check

run:
	$(CONDA_RUN) && python manage.py runserver

migrate:
	$(CONDA_RUN) && python manage.py migrate

makem:
	$(CONDA_RUN) && python manage.py makemigrations

shell:
	$(CONDA_RUN) && python manage.py shell

test:
	$(CONDA_RUN) && python manage.py test

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
