#!/bin/bash
# Auto-index new archive files into RAG DB
# Run via cron: 0 4 * * * /home/simon/.openclaw/workspace/tools/rag-auto-index.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/rag-env/bin/activate"
python3 "$SCRIPT_DIR/rag-engine.py" index-all --dir "$SCRIPT_DIR/../memory/archive"
