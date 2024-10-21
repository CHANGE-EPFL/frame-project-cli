install:
	pip install .[dev]
	pre-commit install

lint:
	pre-commit run --all-files

build:
	python3 -m build

test:
	pytest
