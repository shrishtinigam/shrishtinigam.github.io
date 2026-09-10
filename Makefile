.PHONY: install check build

install:
	python -m pip install -e .

check:
	python -m sitegen.cli check

migrate:
	python -m sitegen.cli migrate

build:
	python -m sitegen.cli build
