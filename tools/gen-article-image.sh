#!/bin/bash
# gen-article-image.sh — Generate a single article image via HF FLUX.1-schnell
# Usage: bash gen-article-image.sh <category> <slug> "<prompt>"
# Example: bash gen-article-image.sh tech 2026-03-13-ai-update "Modern data center with blue LED lights"
set -euo pipefail

CATEGORY="$1"
SLUG="$2"
PROMPT="$3"

HF_API="https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_KEY="${HUGGINGFACE_API_KEY}"
BASE_DIR="${HOME}/.openclaw/workspace/static/images"
OUTPATH="${BASE_DIR}/${CATEGORY}/${SLUG}.jpg"

mkdir -p "${BASE_DIR}/${CATEGORY}"

# Backup if exists
[ -f "$OUTPATH" ] && cp "$OUTPATH" "${OUTPATH}.bak"

STATUS=$(curl -s -o "$OUTPATH" -w "%{http_code}" \
  -X POST "$HF_API" \
  -H "Authorization: Bearer $HF_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"inputs\":\"${PROMPT}\",\"parameters\":{\"width\":1024,\"height\":576}}")

if [ "$STATUS" = "200" ] && [ "$(stat -c%s "$OUTPATH")" -gt 10000 ]; then
  SIZE=$(stat -c%s "$OUTPATH")
  echo "✅ ${CATEGORY}/${SLUG}.jpg (${SIZE} bytes)"
  rm -f "${OUTPATH}.bak"
  exit 0
else
  echo "❌ Failed (HTTP ${STATUS})"
  [ -f "${OUTPATH}.bak" ] && mv "${OUTPATH}.bak" "$OUTPATH"
  exit 1
fi
