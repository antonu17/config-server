VENV ?= venv

.ONESHELL:
.PHONY: setup virtualenv clean

setup: virtualenv requirements

virtualenv:
	$(shell python -m venv $(CURDIR)/$(VENV))

clean:
	@$(shell deactivate)
	@rm -rf $(CURDIR)/$(VENV)

requirements:
	@$(CURDIR)/$(VENV)/bin/pip install -r requirements.txt

lint:
	@$(CURDIR)/$(VENV)/bin/flake8 src/

test:
run:
	FLASK_APP=$(CURDIR)/src/main.py $(CURDIR)/$(VENV)/bin/flask run

build:
artifact:
