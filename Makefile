# Define the directory containing the source code
SRC_DIR := ./src
TEST_DIR := ./tests
EXAMPLE_DIR := ./examples

.PHONY: all
all: test lint build

##@ General

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

.PHONY: install
install: ## Install project dependencies.
	uv pip install --editable .

.PHONY: dev
dev: ## Install development dependencies.
	uv pip install ".[dev]"

.PHONY: test
test: ## Run tests.
	uv run --no-project --no-reinstall pytest $(TEST_DIR) --cov --cov-config=.coveragerc -vv -s

.PHONY: clean
clean: ## Remove build artifacts.
	rm -rf build dist *.egg-info .pytest_cache .coverage

.PHONY: format
format: ## Format code using ruff.
	uv run --no-project --no-reinstall isort $(SRC_DIR) $(TEST_DIR) $(EXAMPLE_DIR)
	uv run --no-project --no-reinstall ruff format $(SRC_DIR) $(TEST_DIR) $(EXAMPLE_DIR); uv run --no-project --no-reinstall ruff check --fix $(SRC_DIR) $(TEST_DIR) $(EXAMPLE_DIR)

.PHONY: lint
lint: ## Run linters using ruff.
	uv run --no-project --no-reinstall ruff format --diff $(SRC_DIR) $(TEST_DIR)
	uv run --no-project --no-reinstall mypy $(SRC_DIR) $(TEST_DIR)

.PHONY: check
check: format lint ## Run format and lint.

##@ Build

.PHONY: build
build: ## Build the application.
	uv build
