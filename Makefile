.PHONY: format check typecheck test

format:
	poetry run ruff format

check:
	poetry run ruff check --fix

typecheck:
	poetry run mypy .

test:
	poetry run python test.py
