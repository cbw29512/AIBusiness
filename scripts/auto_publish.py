#!/usr/bin/env python3
"""
auto_publish.py
Runs the full cycle: scout, build, and commit to GitHub.
This is what runs automatically via cron.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))

import ollama_client as ai
import scout
import builder

def run_cycle():
    """Run one full scout → build cycle and commit to git."""
    print("\n" + "="*60)
    print(f"🤖 AIBusiness Auto-Cycle | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # Check Ollama
    ok, msg = ai.check_connection()
    if not ok:
        print(f"❌ {msg}")
        return False
    print(f"✅ {msg}")
    
    # Scout for problems
    try:
        new_problems = scout.run(3)
        print(f"🔍 Found {len(new_problems)} new problem(s)")
    except Exception as e:
        print(f"⚠️ Scout error: {e}")
        new_problems = []
    
    # Build one product
    try:
        product = builder.run()
        if product:
            print(f"📦 Built: {product['title']} (${product['price_usd']})")
            
            # Generate site
            result = subprocess.run(
                [sys.executable, str(ROOT / "site" / "generate.py")],
                capture_output=True, text=True, cwd=ROOT
            )
            if result.returncode == 0:
                print("✅ Site regenerated")
            
            # Generate Gumroad pages
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "generate_gumroad_page.py")],
                capture_output=True, text=True, cwd=ROOT
            )
            if result.returncode == 0:
                print("✅ Gumroad pages generated")
            
            # Git commit and push
            try:
                subprocess.run(["git", "add", "products/", "index.html", "gumroad_pages/", "state/"], 
                              cwd=ROOT, capture_output=True)
                subprocess.run(["git", "commit", "-m", f"auto: Built {product['title']}"], 
                              cwd=ROOT, capture_output=True)
                subprocess.run(["git", "push", "origin", "main"], 
                              cwd=ROOT, capture_output=True)
                print("🚀 Pushed to GitHub")
                return True
            except Exception as e:
                print(f"⚠️ Git push issue: {e}")
                return False
        else:
            print("📭 No products built this cycle")
            return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

if __name__ == "__main__":
    success = run_cycle()
    sys.exit(0 if success else 1)
