#!/bin/bash

export UV_CACHE_DIR="/goinfre/ihasbi/.cache/uv"
export UV_PROJECT_ENVIRONMENT="/goinfre/ihasbi/call_me_maybe/.venv"
export HF_HOME="/goinfre/ihasbi/.cache/huggingface"
export TRANSFORMERS_CACHE="/goinfre/ihasbi/.cache/huggingface"

echo "Environment variables set:"
echo "UV_CACHE_DIR=$UV_CACHE_DIR"
echo "UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT"
echo "HF_HOME=$HF_HOME"
echo "TRANSFORMERS_CACHE=$TRANSFORMERS_CACHE"
