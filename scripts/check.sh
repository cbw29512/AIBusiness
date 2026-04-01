#!/usr/bin/env bash
# check.sh — Diagnose the AIBusiness setup
# Run this first to see what's working and what needs attention.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo ""
echo "🔎 AIBusiness Setup Check"
echo "================================"
echo ""

# Ollama
echo "1. Ollama"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "
import json,sys
data=json.load(sys.stdin)
models=[m['name'] for m in data.get('models',[])]
print(', '.join(models) if models else 'NO MODELS INSTALLED')
" 2>/dev/null)
  echo "   ✅ Running — models: $MODELS"
  if [ "$MODELS" = "NO MODELS INSTALLED" ]; then
    echo "   ⚠️  No models! Run: ollama pull llama3.2"
  fi
else
  echo "   ❌ Not running — start it: ollama serve"
fi

echo ""

# Python
echo "2. Python"
if command -v python3 > /dev/null 2>&1; then
  echo "   ✅ $(python3 --version)"
else
  echo "   ❌ Python 3 not found — install from python.org"
fi

echo ""

# Products
echo "3. Products"
COUNT=$(ls -d "$ROOT/products"/*/ 2>/dev/null | wc -l | tr -d ' ')
echo "   📦 $COUNT product(s) in library"
if [ "$COUNT" -gt "0" ]; then
  ls -d "$ROOT/products"/*/ 2>/dev/null | while read dir; do
    name=$(basename "$dir")
    status=$(python3 -c "import json; d=json.load(open('$dir/listing.json')); print(d.get('status','?'))" 2>/dev/null || echo "?")
    price=$(python3 -c "import json; d=json.load(open('$dir/listing.json')); print(d.get('price_usd','?'))" 2>/dev/null || echo "?")
    url=$(python3 -c "import json; d=json.load(open('$dir/listing.json')); print('live' if d.get('listing_url') else 'no url')" 2>/dev/null || echo "?")
    echo "     • $name — \$$price [$status, $url]"
  done
fi

echo ""

# GitHub
echo "4. GitHub"
if [ -d "$ROOT/.git" ]; then
  REMOTE=$(git -C "$ROOT" remote get-url origin 2>/dev/null || echo "no remote")
  echo "   ✅ Git repo exists — remote: $REMOTE"
else
  echo "   ○ No git repo yet — see README for GitHub Pages setup"
fi

echo ""

# Site
echo "5. Site"
if [ -f "$ROOT/index.html" ]; then
  MODIFIED=$(date -r "$ROOT/index.html" "+%Y-%m-%d %H:%M" 2>/dev/null || echo "unknown")
  echo "   ✅ index.html exists (last built: $MODIFIED)"
else
  echo "   ○ index.html not yet generated — run: python3 site/generate.py"
fi

echo ""

# Gumroad
echo "6. Gumroad"
GUMROAD=$(python3 -c "import json; c=json.load(open('$ROOT/config.json')); print(c['business'].get('gumroad_username','') or 'NOT SET')" 2>/dev/null)
if [ "$GUMROAD" != "NOT SET" ]; then
  echo "   ✅ Username: $GUMROAD"
else
  echo "   ○ Not configured — add your Gumroad username to config.json"
fi

echo ""
echo "================================"
echo "Run ./scripts/start.sh to begin"
echo ""
