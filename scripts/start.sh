#!/usr/bin/env bash
# start.sh — Start the AIBusiness engine
#
# Usage:
#   ./scripts/start.sh          # run once (test)
#   ./scripts/start.sh loop     # run continuously every 60 minutes
#   ./scripts/start.sh loop 45  # run every 45 minutes

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo ""
echo "🚀 AIBusiness Engine"
echo "================================"

# Check Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo ""
  echo "❌ Ollama is not running."
  echo ""
  echo "   Fix: Open a NEW Terminal tab and run:"
  echo "   ollama serve"
  echo ""
  echo "   Then come back and run this script again."
  exit 1
fi

echo "✅ Ollama is running"
echo ""

MODE="${1:-once}"
INTERVAL="${2:-60}"

if [ "$MODE" = "loop" ]; then
  echo "🔄 Running in loop mode (every ${INTERVAL} minutes)"
  echo "   Press Ctrl+C to stop"
  echo ""
  python3 engine/loop.py --loop "$INTERVAL"
else
  echo "🔄 Running one cycle..."
  echo ""
  python3 engine/loop.py
fi
