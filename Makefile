install:
	pip install -e .[dev]
	pre-commit install -t pre-commit -t commit-msg

lint:
	pre-commit run --all-files

build:
	python3 -m build

test:
	pytest
