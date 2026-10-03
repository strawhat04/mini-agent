.PHONY: setup_tool help

help:
	@echo "Available commands:"
	@echo "  make setup_tool - Check and install uv and ruff"

setup_tool:
	@if ! uv --version >/dev/null 2>&1; then \
		echo "uv not found. Installing uv ...."; \
		curl -sSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "uv is already installed"; \
	fi
	@# Check ruff next
	@if ! ruff --version >/dev/null 2>&1; then \
		echo "ruff not found. Installing ruff ...."; \
		uv tool install ruff; \
	else \
		echo "ruff is already installed"; \
	fi