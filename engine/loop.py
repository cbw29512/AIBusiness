#!/usr/bin/env python3
"""
loop.py
The main AIBusiness engine loop.

Each cycle:
  1. Scout — find 3 fixable business problems
  2. Build — generate the digital fix for 1 problem using local Ollama AI
  3. Generate site — rebuild index.html
  4. Deploy — git push to GitHub Pages (if configured)
  5. Sleep — wait before next cycle

Usage:
  python3 engine/loop.py              # run once
  python3 engine/loop.py --loop 60   # run every 60 minutes
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))

import ollama_client as ai
import scout
import builder
import updater

# Gumroad publisher (optional — skips gracefully if token not set)
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
try:
    import publish_to_gumroad as gumroad
    GUMROAD_AVAILABLE = True
except ImportError:
    GUMROAD_AVAILABLE = False

CONFIG = json.loads((ROOT / "config.json").read_text())
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    (LOG_DIR / "loop.log").open("a").write(line + "\n")


def generate_site():
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "site" / "generate.py")],
            capture_output=True, text=True, cwd=ROOT
        )
        if result.returncode == 0:
            log("✅ Site regenerated")
        else:
            log(f"⚠️  Site generation warning: {result.stderr[:200]}")
    except Exception as e:
        log(f"❌ Site generation failed: {e}")


def deploy_to_github(message: str = ""):
    if not CONFIG["deploy"].get("auto_deploy"):
        return
    if not (ROOT / ".git").exists():
        log("⚠️  No git repo — skipping deploy (see README for GitHub setup)")
        return

    try:
        subprocess.run(["git", "add", "index.html", "products/"], cwd=ROOT, capture_output=True)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if diff.returncode == 0:
            log("   No site changes to deploy")
            return

        commit_msg = message or f"update: AI cycle {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=ROOT, capture_output=True)
        result = subprocess.run(["git", "push", "origin", "main"], cwd=ROOT, capture_output=True, text=True)

        if result.returncode == 0:
            log("🚀 Deployed to GitHub Pages")
        else:
            log(f"⚠️  Push failed: {result.stderr[:200]}")
    except Exception as e:
        log(f"❌ Deploy error: {e}")


def run_cycle():
    """Run one full scout → build → generate → deploy cycle."""
    log("=" * 50)
    log("🔄 CYCLE START")

    # Check Ollama is up
    ok, msg = ai.check_connection()
    if not ok:
        log(f"❌ Ollama not available: {msg}")
        log("   Start Ollama: open Terminal → run 'ollama serve'")
        return False

    log(f"🤖 {msg}")

    # Scout for problems
    try:
        n = CONFIG["scout"].get("problems_per_cycle", 3)
        new_problems = scout.run(n)
        log(f"🔍 Scout found {len(new_problems)} new problem(s)")
    except Exception as e:
        log(f"⚠️  Scout error: {e}")

    # Build one product
    try:
        product = builder.run()
        if product:
            log(f"📦 Built: {product['title']} — ${product['price_usd']}")

            # Publish to Gumroad → get real buy links before regenerating site
            if GUMROAD_AVAILABLE:
                try:
                    published = gumroad.run()
                    if published:
                        log(f"🛒 Published {published} product(s) to Gumroad")
                    else:
                        log("🛒 Gumroad: nothing new to publish (or already live)")
                except Exception as ge:
                    log(f"⚠️  Gumroad publish error: {ge}")

            generate_site()
            deploy_to_github(f"add: {product['title']}")
        else:
            log("📭 Nothing to build this cycle")
    except Exception as e:
        log(f"❌ Build error: {e}")

    # Update one existing product (re-research + refresh content + new prompts)
    try:
        updated = updater.run()
        if updated:
            log(f"🔄 Updated: {updated['title']} → v{updated.get('version', '?')}")

            # Re-publish updated PDF to Gumroad
            if GUMROAD_AVAILABLE:
                try:
                    product_dir = ROOT / "products" / updated["slug"]
                    if product_dir.exists():
                        gumroad_id = updated.get("gumroad_id")
                        pdf_name   = updated.get("pdf_file", f"{updated['slug']}.pdf")
                        pdf_path   = product_dir / pdf_name
                        if gumroad_id and pdf_path.exists():
                            ok = gumroad.upload_pdf(gumroad_id, pdf_path)
                            if ok:
                                log(f"📤 Re-uploaded updated PDF to Gumroad")
                except Exception as ge:
                    log(f"⚠️  Gumroad re-upload error: {ge}")

            generate_site()
            deploy_to_github(f"update: {updated['title']} v{updated.get('version', '?')}")
        else:
            log("🔄 Updater: all products are current")
    except Exception as e:
        log(f"⚠️  Updater error: {e}")

    log("✅ CYCLE COMPLETE")
    return True


def main():
    args = sys.argv[1:]
    loop_mode = "--loop" in args
    interval = 60  # minutes

    if loop_mode:
        try:
            idx = args.index("--loop")
            interval = int(args[idx + 1]) if idx + 1 < len(args) else 60
        except (ValueError, IndexError):
            interval = 60

    log(f"🚀 AIBusiness Engine starting")
    log(f"   Mode: {'continuous loop every ' + str(interval) + ' min' if loop_mode else 'single cycle'}")
    log(f"   Root: {ROOT}")

    if loop_mode:
        while True:
            run_cycle()
            log(f"💤 Sleeping {interval} minutes...")
            time.sleep(interval * 60)
    else:
        run_cycle()


if __name__ == "__main__":
    main()
