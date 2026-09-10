.PHONY: install check build

install:
	python -m pip install -e .

check:
	python -m sitegen.cli check

test:
	python -m unittest discover -s tests -v

migrate:
	python -m sitegen.cli migrate

build:
	python -m sitegen.cli build
