VENV ?= venv

.ONESHELL:
.PHONY: setup virtualenv clean requirements-dev requirements lint test run build artifact

setup: virtualenv requirements-dev

virtualenv:
	@python -m venv $(CURDIR)/$(VENV)

clean:
	@rm -rf $(CURDIR)/$(VENV)

requirements-dev:
	@$(CURDIR)/$(VENV)/bin/pip install -r requirements-dev.txt

requirements:
	@$(CURDIR)/$(VENV)/bin/pip install -r requirements.txt

lint:
	@$(CURDIR)/$(VENV)/bin/flake8 src/ tests/

test:
	@$(CURDIR)/$(VENV)/bin/python -m pytest tests/ -v

run: setup
	FLASK_APP=$(CURDIR)/src/main.py $(CURDIR)/$(VENV)/bin/flask run

build:
artifact:
