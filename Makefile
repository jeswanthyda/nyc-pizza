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

# Run the FastAPI backend server
run_backend_server:
	uv run python run_backend.py

# Run the NYC Pizza game (requires backend to be running)
run_game:
	uv run python main.py
