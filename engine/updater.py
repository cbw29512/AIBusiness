#!/usr/bin/env python3
"""
updater.py
Keeps existing products current — re-researches topics, adds new AI prompts,
refreshes viral content angles, and rebuilds the PDF when better info is found.

Each cycle, the loop picks the product that hasn't been updated longest
and runs it through this pipeline:

  1. Re-research — fetch latest tool docs and trending angles
  2. Compare — ask Ollama: "What's new or missing vs. this existing guide?"
  3. Merge — rewrite stale sections, add new steps or prompts
  4. Rebuild PDF — new version with "Updated [date]" on cover
  5. Re-upload — push new PDF to Gumroad, update listing description
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))

import ollama_client as ai
import researcher
import pdf_generator as pdfgen

PRODUCTS_DIR = ROOT / "products"
UPDATE_AFTER_DAYS = 7   # re-check products older than this many days
MIN_SCORE_TO_UPDATE = 3  # Ollama must score the new research ≥ this to trigger rewrite


# ── Ollama prompt templates ───────────────────────────────────────────────────

REVIEWER_SYSTEM = """You are a content quality reviewer for small-business guides.
Your job is to compare an existing guide with fresh research and decide:
1. What useful NEW information exists in the research that's not in the guide
2. Which steps in the guide are now outdated or could be more specific
3. What new AI prompts would genuinely help a non-technical business owner

Be specific and honest. If the guide is already excellent and the research adds nothing new,
say so — don't invent improvements just to justify an update.
Reply only with valid JSON."""

MERGER_SYSTEM = """You are rewriting sections of a small-business guide to add new,
current information. Rules:
1. Keep the same plain-English, non-technical tone — buyers are NOT tech people
2. Name every button click with the exact text shown on screen in "quotes"
3. Tell readers what they'll see after each step
4. Only include information that is accurate and verified — no guessing
5. Numbered steps only (sub-steps use letters: 1a, 1b)
6. Add new information naturally — don't just append it at the end
7. Keep the same section headers exactly
8. Be friendly and confident, like explaining to a smart friend"""

PROMPT_UPDATER_SYSTEM = """You write AI prompts that non-technical small business owners
can copy and paste into ChatGPT or Claude to get real work done.

Rules for each prompt:
- Start with a plain English instruction line in [square brackets] explaining what it does
- Use [BRACKETS] for the parts the user should customise (e.g. [your business name])
- Every prompt must produce something concrete: a written piece, a list, a plan, a template
- Prompts must be self-contained — the user shouldn't need anything else
- Tone: friendly and direct. No jargon.
- Focus on what's trending right now: viral hooks, AI-optimised copy, platform-specific tactics

Reply only with valid JSON."""


# ── core functions ────────────────────────────────────────────────────────────

def needs_update(listing: dict) -> bool:
    """Returns True if the product is due for an update."""
    if listing.get("frozen"):   # manual override to skip updating
        return False
    if listing.get("status") != "live":
        return False            # don't update products that haven't launched yet

    last = listing.get("last_updated") or listing.get("created_at", "")
    if not last:
        return True

    try:
        last_dt = datetime.fromisoformat(last)
        return datetime.now() - last_dt > timedelta(days=UPDATE_AFTER_DAYS)
    except ValueError:
        return True


def pick_product_to_update() -> Optional[Path]:
    """Return the product directory that most needs an update."""
    if not PRODUCTS_DIR.exists():
        return None

    candidates = []
    for d in PRODUCTS_DIR.iterdir():
        if not d.is_dir():
            continue
        lf = d / "listing.json"
        if not lf.exists():
            continue
        listing = json.loads(lf.read_text())
        if needs_update(listing):
            last = listing.get("last_updated") or listing.get("created_at", "1970-01-01")
            candidates.append((last, d))

    if not candidates:
        return None
    # Oldest first
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]


def research_update_angles(listing: dict) -> str:
    """Re-research the topic for fresh content and trending angles."""
    # Build a synthetic problem dict from the listing so researcher can use it
    problem = {
        "category": listing.get("category", ""),
        "problem_statement": listing.get("description", ""),
        "why_fixable": listing.get("tagline", ""),
        "product_title": listing.get("title", ""),
        "who_has_it": listing.get("who_its_for", ""),
    }
    context = researcher.research_for_problem(problem)

    # Also add a trending-angles query hint so the AI thinks about virality
    trending_hint = (
        "\n\nADDITIONAL CONTEXT FOR UPDATE:\n"
        "When suggesting improvements, also consider:\n"
        "- Viral content formats that are working right now (e.g. before/after, '3 mistakes', '5-minute fix')\n"
        "- New AI tools or features released in 2025-2026 that make this easier\n"
        "- Common questions buyers ask after purchasing (what they still struggle with)\n"
        "- Short-form video hooks and social proof angles that convert well\n"
    )
    return context + trending_hint


def score_update(existing_guide: str, new_research: str, listing: dict, model: str) -> dict:
    """
    Ask Ollama to review the existing guide against new research.
    Returns a score and list of specific improvements.
    """
    prompt = f"""Here is an existing guide called "{listing['title']}":

--- EXISTING GUIDE (first 2000 chars) ---
{existing_guide[:2000]}
--- END GUIDE ---

Here is fresh research and trending information on this topic:
{new_research[:2000]}

Review the guide against the new research. Return JSON:
{{
  "update_score": <integer 1-10, where 1=nothing new, 10=major improvements needed>,
  "new_sections": [<list of specific new topics or steps to add>],
  "outdated_sections": [<list of sections that need updating with reason>],
  "new_prompt_ideas": [<list of 2-3 new AI prompt concepts that would help buyers>],
  "viral_angles": [<list of 1-2 viral content formats that fit this product>],
  "summary": "<one sentence explaining the most valuable update>"
}}"""

    result = ai.generate_json(prompt, REVIEWER_SYSTEM, model)
    if not result:
        return {"update_score": 0}
    return result


def rewrite_guide(existing_guide: str, review: dict, new_research: str,
                  listing: dict, model: str) -> str:
    """
    Merge improvements into the existing guide. Returns the updated guide text.
    """
    new_sections_txt = "\n".join(f"- {s}" for s in review.get("new_sections", []))
    outdated_txt     = "\n".join(f"- {s}" for s in review.get("outdated_sections", []))
    viral_txt        = "\n".join(f"- {s}" for s in review.get("viral_angles", []))

    prompt = f"""Rewrite and improve this guide for "{listing['title']}".

ORIGINAL GUIDE:
{existing_guide}

NEW RESEARCH TO INCORPORATE:
{new_research[:1500]}

SPECIFIC IMPROVEMENTS TO MAKE:
New sections/topics to add:
{new_sections_txt or '(none)'}

Sections to update or make more specific:
{outdated_txt or '(none)'}

Viral content angles to mention in the Quick Win section:
{viral_txt or '(none)'}

Rewrite the complete guide with these improvements built in naturally.
Keep all 6 section headers exactly: THE PROBLEM, WHAT YOU'LL HAVE WHEN YOU'RE DONE,
WHAT YOU NEED BEFORE YOU START, STEP-BY-STEP SETUP, WHAT TO DO IF SOMETHING GOES WRONG,
QUICK WIN

Write for non-technical small business owners. Every step must name the exact button text
in "quotes" and tell readers what they'll see afterwards."""

    updated = ai.generate(prompt, MERGER_SYSTEM, model)
    return updated.strip() if updated else existing_guide


def generate_fresh_prompts(listing: dict, updated_guide: str,
                           review: dict, model: str) -> list:
    """Generate a refreshed AI prompt library including trending prompt patterns."""
    viral_angles = review.get("viral_angles", [])
    new_ideas    = review.get("new_prompt_ideas", [])

    prompt = f"""Create 6 ready-to-use AI prompts for buyers of "{listing['title']}".

Product context: {listing.get('description', '')}
Who uses it: {listing.get('who_its_for', 'small business owners')}

Trending prompt ideas to include:
{chr(10).join('- ' + i for i in new_ideas) if new_ideas else '(use your best judgement)'}

Viral content angles to cover:
{chr(10).join('- ' + v for v in viral_angles) if viral_angles else '(use your best judgement)'}

Also include prompts for:
- Writing a before/after social post about their results
- Getting ChatGPT to spot the #1 thing slowing them down
- Turning their new system into a client pitch or upsell

Return JSON array:
[
  {{
    "label": "short name for this prompt",
    "use_case": "one sentence: what the buyer will get from running this",
    "prompt": "the full prompt text with [BRACKETS] for customisation"
  }}
]"""

    result = ai.generate_json(prompt, PROMPT_UPDATER_SYSTEM, model)
    if isinstance(result, list):
        return result
    return []


def bump_version(listing: dict) -> dict:
    """Increment version number and set last_updated timestamp."""
    listing = dict(listing)
    current = listing.get("version", 1)
    try:
        current = int(current)
    except (TypeError, ValueError):
        current = 1
    listing["version"]      = current + 1
    listing["last_updated"] = datetime.now().isoformat()

    history = listing.get("update_history", [])
    history.append({
        "version": listing["version"],
        "date":    listing["last_updated"][:10],
    })
    listing["update_history"] = history[-10:]   # keep last 10
    return listing


# ── main entry point ──────────────────────────────────────────────────────────

def update_product(product_dir: Path, model: Optional[str] = None) -> Optional[dict]:
    """
    Full update pipeline for one product.
    Returns the updated listing dict, or None if no update was needed/possible.
    """
    listing_file = product_dir / "listing.json"
    guide_file   = product_dir / "guide.txt"

    if not listing_file.exists() or not guide_file.exists():
        return None

    listing       = json.loads(listing_file.read_text())
    existing_guide = guide_file.read_text()

    if model is None:
        model = ai.get_best_model()
    if model is None:
        print("   ❌ No Ollama model available")
        return None

    title = listing.get("title", product_dir.name)
    print(f"\n🔄 Checking for updates: {title}")

    # 1. Re-research
    print("   🌐 Fetching latest research...")
    new_research = research_update_angles(listing)
    if not new_research:
        print("   ⚠️  No new research found — skipping")
        return None

    # 2. Score the update opportunity
    print("   🤔 Reviewing against current guide...")
    review = score_update(existing_guide, new_research, listing, model)
    score  = review.get("update_score", 0)
    print(f"   📊 Update score: {score}/10 — {review.get('summary', '')}")

    if score < MIN_SCORE_TO_UPDATE:
        print(f"   ✅ Guide is current — no update needed (score {score} < {MIN_SCORE_TO_UPDATE})")
        # Still bump the checked timestamp so we don't re-check every cycle
        listing["last_updated"] = datetime.now().isoformat()
        listing_file.write_text(json.dumps(listing, indent=2))
        return None

    # 3. Rewrite guide with improvements
    print(f"   ✍️  Rewriting guide with {len(review.get('new_sections', []))} new section(s)...")
    updated_guide = rewrite_guide(existing_guide, review, new_research, listing, model)

    # 4. Generate fresh prompts
    print("   🤖 Generating updated AI prompt library...")
    fresh_prompts = generate_fresh_prompts(listing, updated_guide, review, model)
    print(f"      {len(fresh_prompts)} prompt(s) generated")

    # 5. Rebuild PDF with new version number
    listing = bump_version(listing)
    version = listing["version"]
    print(f"   📄 Rebuilding PDF (v{version})...")

    slug     = listing.get("slug", product_dir.name)
    pdf_path = product_dir / f"{slug}.pdf"

    try:
        pdfgen.build_pdf(listing, updated_guide, fresh_prompts, str(pdf_path))
        print(f"      PDF written → {pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)")
    except Exception as e:
        print(f"   ⚠️  PDF rebuild failed: {e}")

    # 6. Save everything
    guide_file.write_text(updated_guide)
    (product_dir / "prompts.json").write_text(json.dumps(fresh_prompts, indent=2))

    listing["prompt_count"] = len(fresh_prompts)
    listing_file.write_text(json.dumps(listing, indent=2))

    print(f"   ✅ Updated to v{version} — {listing['last_updated'][:10]}")
    return listing


def run() -> dict | None:
    """
    Pick the most stale product and update it.
    Returns updated listing or None. Called by loop.py.
    """
    product_dir = pick_product_to_update()
    if not product_dir:
        return None

    model = ai.get_best_model()
    return update_product(product_dir, model)


if __name__ == "__main__":
    import sys
    # Allow targeting a specific product: python3 engine/updater.py products/my-product
    if len(sys.argv) > 1:
        target = ROOT / sys.argv[1]
        if target.is_dir():
            update_product(target)
        else:
            print(f"❌ Not found: {target}")
    else:
        result = run()
        if not result:
            print("Nothing to update right now.")
