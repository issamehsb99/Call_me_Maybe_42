PYTHON := python3
MAIN := src

.PHONY: setup install run debug clean lint lint-strict check cache-info

setup:
	mkdir -p $(UV_CACHE_DIR)
	mkdir -p $(HF_HOME)
	uv sync

install:
	uv sync
run:
	uv run --no-active $(PYTHON) -m $(MAIN)

debug:
	uv run --no-active $(PYTHON) -m pdb -m $(MAIN)


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true


lint:
	uv run --no-active flake8 .
	uv run --no-active mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs