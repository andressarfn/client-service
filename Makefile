PROJECT_NAME := $(notdir $(CURDIR))

deps:
	poetry install
	poetry run pre-commit install

# Lint code
lint:
	black . --check --diff
	flake8 src --max-complexity=6
	isort . --check-only --diff
	ruff check .

format:
	black .
	isort .
	ruff check . --fix

start: check-deps
	uvicorn src.main:app --port 8081 --loop uvloop --reload

create-env:
	cp .env.example .env
	@echo "Created .env file from .env.example. Please review and update it as necessary."

check-deps:
	@if [ ! -f ".env" ]; then \
		echo "IMPORTANT: The .env file is not found, please create it based on the .env.example file."; \
		echo "Starting the application with the following configuration:"; \
		cat .env.example; \
		exit 1; \
	fi
