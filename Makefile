VENV         ?= venv
BUILD_DIR    ?= build
SRC_DIR      ?= src
TESTS_DIR    ?= tests
DOCKER_REPO  ?= config-server
VERSION      ?= $(shell git describe --tags --always --dirty)

.ONESHELL:
.PHONY: setup virtualenv clean requirements-dev requirements lint test run build artifact

setup: virtualenv requirements-dev

virtualenv:
	@python3 -m venv $(VENV)

clean:
	@rm -rf $(VENV)
	@rm -rf $(BUILD_DIR)
	@rm -rf $(SRC_DIR)/__pycache__

requirements-dev:
	@$(VENV)/bin/pip install -r requirements-dev.txt

requirements:
	@$(VENV)/bin/pip install -r requirements.txt

lint: virtualenv requirements-dev
	@$(VENV)/bin/flake8 $(SRC_DIR) $(TESTS_DIR)

test: virtualenv requirements-dev
	@$(VENV)/bin/python -m pytest $(TESTS_DIR) -v

run: virtualenv requirements-dev
	$(VENV)/bin/uwsgi --http 127.0.0.1:5000 --wsgi-file $(SRC_DIR)/main.py --callable app_dispatch

build: virtualenv requirements
	@mkdir -p $(BUILD_DIR)
	@cp -a $(VENV) $(BUILD_DIR)
	@cp -a $(SRC_DIR)/* $(BUILD_DIR)
	@echo $(VERSION) >$(BUILD_DIR)/version.txt

artifact:
	docker build --rm --tag "$(DOCKER_REPO):$(VERSION)" --build-arg VERSION="$(VERSION)" .
