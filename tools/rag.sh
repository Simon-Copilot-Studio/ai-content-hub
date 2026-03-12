#!/bin/bash
# RAG Engine wrapper - activates venv and runs rag-engine.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/rag-env/bin/activate"
python3 "$SCRIPT_DIR/rag-engine.py" "$@"
