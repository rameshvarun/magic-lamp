.PHONY: format

format:
	poetry run ruff format

typecheck:
	poetry run mypy .
