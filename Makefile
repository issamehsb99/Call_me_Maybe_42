PYTHON := python3
MAIN := src

export UV_CACHE_DIR := /goinfre/ihasbi/.cache/uv
export UV_PROJECT_ENVIRONMENT := /goinfre/ihasbi/call_me_maybe/.venv

export HF_HOME := /goinfre/ihasbi/.cache/huggingface
export HF_HUB_CACHE := /goinfre/ihasbi/.cache/huggingface/hub
export TRANSFORMERS_CACHE := /goinfre/ihasbi/.cache/huggingface

export HF_HUB_DOWNLOAD_TIMEOUT := 600
export HF_HUB_ETAG_TIMEOUT := 60

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

check:
	uv run --no-active $(PYTHON) -c "import pydantic, numpy; print('Dependencies OK')"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

cache-info:
	@echo "UV cache: $(UV_CACHE_DIR)"
	@echo "Virtual environment: $(UV_PROJECT_ENVIRONMENT)"
	@echo "Hugging Face cache: $(HF_HOME)"
	@du -sh $(HF_HOME) 2>/dev/null || true

lint:
	uv run --no-active flake8 .
	uv run --no-active mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs