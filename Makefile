.PHONY: format check typecheck

format:
	poetry run ruff format

check:
	poetry run ruff check --fix

typecheck:
	poetry run mypy .
