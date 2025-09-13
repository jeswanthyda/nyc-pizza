.PHONY: format lint check install

# Format code using ruff
format:
	uv run ruff format .

# Lint code using ruff
lint:
	uv run ruff check .

# Check and fix linting issues automatically
check:
	uv run ruff check --fix .

# Install dependencies
install:
	uv sync

# Run all checks (format + lint)
all: format lint
