.PHONY: format check typecheck test docker-shell

format:
	poetry run ruff format

check:
	poetry run ruff check --fix

typecheck:
	poetry run mypy .

test:
	poetry run python test.py

docker-shell:
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/magic-lamp \
		--mount type=bind,source="$(HOME)/.cache/huggingface/",target=/root/.cache/huggingface \
		-w /magic-lamp \
		-it python:3.9 \
		bash