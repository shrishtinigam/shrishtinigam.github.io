.PHONY: install check build

install:
	python -m pip install -e .

check:
	python -m sitegen.cli check

build:
	python -m sitegen.cli build
