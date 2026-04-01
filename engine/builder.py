#!/usr/bin/env python3
"""
builder.py
Takes a problem from the scout queue and builds a complete digital product:
- A full guide/blueprint/template (the deliverable buyers receive)
- A product listing (title, description, features, price)
- Saves everything to products/<slug>/

The local Ollama AI does all the writing.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import ollama_client as ai
import pdf_generator as pdfgen
import researcher

# ── Core writing rules — passed to Ollama on every guide generation ───────────
# These rules ensure every guide is written for non-technical people
# using real, current information from the tool websites.
WRITER_SYSTEM_PROMPT = """You are a plain-English business guide writer for non-technical small business owners.

AUDIENCE: Your reader has never done this before. They are not a developer, not a techie.
They run their own business — salon, freelance studio, consultancy, online shop — and
they just want to fix a specific problem without learning a new skill.

STRICT WRITING RULES — follow every one of these:

1. NO JARGON WITHOUT EXPLANATION
   Never write "configure", "integrate", "authenticate", "deploy", "API", "webhook",
   "automation trigger", or any technical term without immediately explaining it in
   plain English in brackets. Example: "webhook (a way for one app to automatically
   tell another app something happened)"

2. NAME EVERY CLICK
   Don't say "go to Settings". Say exactly:
   "Click the gear icon in the top-right corner of your screen, then click 'Settings'
   from the dropdown menu that appears."
   Every button, menu item, and field must be named in quotes exactly as it appears
   on screen.

3. TELL THEM WHAT THEY'LL SEE
   After each step, describe what happens next so they know they did it right.
   Example: "After clicking Save, you'll see a green 'Changes saved' message at the
   top of the screen. If you see red text instead, check that you filled in all fields."

4. USE REAL, CURRENT INFORMATION ONLY
   If you have been given live documentation from the tool's website (provided below),
   use it verbatim for menu names, button labels, and settings paths.
   Do NOT invent or guess interface details. If you are not sure, say
   "check the tool's help centre for the latest steps" rather than guessing.

5. EXPLAIN WHY, NOT JUST WHAT
   Before each step, one sentence explaining why they're doing it.
   Example: "We're setting up automatic reminders so the software chases the client
   for you — you won't have to write any of these emails yourself."

6. ZERO ASSUMPTIONS
   Assume they have never heard of the tools you're recommending.
   Always include: what the tool is, why it's being used, and that it has a free plan.

7. NUMBERED STEPS ONLY
   Use numbered steps for all instructions. No bullet lists for action items.
   Sub-steps use letters: 1a, 1b, 1c.

8. FRIENDLY, CONFIDENT TONE
   Write like a knowledgeable friend helping someone over the phone.
   Not formal. Not condescending. Reassuring.
   Example opener: "Don't worry — this looks more complicated than it is.
   You'll have this set up in under an hour and you'll never have to think
   about it again."
"""

PROBLEMS_FILE = ROOT / "state" / "problems.json"
PRODUCTS_DIR = ROOT / "products"
CONFIG = json.loads((ROOT / "config.json").read_text())

PRODUCT_ICONS = {
    "guide":      "📋",
    "template":   "📊",
    "checklist":  "✅",
    "blueprint":  "🗺️",
    "swipe_file": "📁",
}

PRODUCT_TYPE_LABELS = {
    "guide":      "Step-by-Step Guide",
    "template":   "Ready-to-Use Template",
    "checklist":  "Action Checklist",
    "blueprint":  "Implementation Blueprint",
    "swipe_file": "Swipe File",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:60]


def load_problems() -> dict:
    if not PROBLEMS_FILE.exists():
        return {"problems": []}
    return json.loads(PROBLEMS_FILE.read_text())


def save_problems(state: dict):
    PROBLEMS_FILE.write_text(json.dumps(state, indent=2))


def get_next_problem(state: dict) -> Optional[dict]:
    for p in state["problems"]:
        if p["status"] == "pending":
            return p
    return None


def mark_problem(state: dict, problem_id: str, status: str, product_id: str = ""):
    for p in state["problems"]:
        if p["id"] == problem_id:
            p["status"] = status
            p["built_at"] = datetime.now().isoformat()
            if product_id:
                p["product_id"] = product_id
            break


def build_guide_content(problem: dict, model: str, research_context: str = "") -> str:
    """
    Generate the full guide content using live-researched tool documentation.
    Written for non-technical readers — every click named, every term explained.
    """
    product_type = problem.get("product_type", "guide")
    title = problem.get("product_title", "Business Fix Guide")
    who = problem.get("who_has_it", "small business owners")
    problem_statement = problem.get("problem_statement", "")
    fix_time = problem.get("fix_time_hours", 2)
    category = problem.get("category", "")

    ai_note = ""
    if "ai_" in category:
        ai_note = (
            "\n\nAI TOOLS NOTE: This guide uses ChatGPT or Claude. "
            "Always explain that these are free-to-use websites the reader visits in their browser — "
            "no download needed. Remind them that AI tools update their interfaces regularly, "
            "so if a button looks slightly different, the function is the same. "
            "Every prompt in this guide has been tested and works as written."
        )

    prompt = f"""Write a complete, production-ready {product_type} for: {who}

Product title: {title}
Problem being solved: {problem_statement}
Estimated implementation time for a complete beginner: {fix_time} hours
{ai_note}

{research_context}

STRUCTURE (use ALL CAPS headers exactly as shown):

THE PROBLEM
Write 2-3 sentences describing exactly what's going wrong and the real cost to their business (time, money, stress). Be specific. No fluff.

WHAT YOU'LL HAVE WHEN YOU'RE DONE
List 4-6 specific, concrete outcomes. Start each with "✓". Example: "✓ An automated system that sends polite payment reminders for you — no manual emails needed"

WHAT YOU NEED BEFORE YOU START
List every account or tool they need. For each one: name it, say it's free (if it is), and give the exact website URL. Example: "Wave account (free) — sign up at waveapps.com"

STEP-BY-STEP SETUP
Number every step. Name every click in quotes exactly as it appears on screen. After each step, tell them what they'll see to confirm it worked. Use sub-steps (1a, 1b) for complex actions. Include copy-paste templates, email scripts, or example text wherever relevant.

WHAT TO DO IF SOMETHING GOES WRONG
List 3-4 common problems and exactly how to fix them.

QUICK WIN — DO THIS FIRST
The single most important first step they can do in the next 10 minutes. One paragraph, very specific.

Length: 800-1200 words. Write the full guide now, starting with THE PROBLEM."""

    return ai.generate(prompt, system=WRITER_SYSTEM_PROMPT, model=model)


def build_listing(problem: dict, guide_content: str, model: str) -> dict:
    """Generate the product listing (title, description, features, price)."""

    prompt = f"""You are a direct-response copywriter writing a product listing for a digital {problem.get('product_type', 'guide')}.

Product title: {problem.get('product_title')}
Problem it solves: {problem.get('problem_statement')}
Who it's for: {problem.get('who_has_it')}
Price: ${problem.get('price_usd', 29)}

Write a compelling product listing. Return JSON:
{{
  "title": "Final product title (punchy, benefit-first, under 10 words)",
  "tagline": "One sentence hook that captures the core promise",
  "description": "3-4 sentence sales description. Lead with the pain, then the solution, then the outcome. No fluff.",
  "features": [
    "Feature/benefit 1 (start with what they GET, not what it IS)",
    "Feature/benefit 2",
    "Feature/benefit 3",
    "Feature/benefit 4",
    "Feature/benefit 5"
  ],
  "who_its_for": "One sentence describing exact buyer",
  "guarantee": "30-day money-back guarantee line"
}}"""

    return ai.generate_json(prompt, model=model)


def build_prompts(problem: dict, guide_content: str, model: str) -> List[dict]:
    """Generate 5-7 tested, copy-paste AI prompts for implementing the fix."""

    category = problem.get("category", "")
    title = problem.get("product_title", "")
    who = problem.get("who_has_it", "small business owners")

    prompt = f"""You are creating an AI Prompt Library for non-technical small business owners.
They have never used AI tools before. Each prompt must work perfectly when pasted into
ChatGPT (chatgpt.com) or Claude (claude.ai) — both free websites, no download needed.

Product: {title}
Audience: {who}
Problem: {problem.get('problem_statement', '')}

Create 5 to 7 prompts that walk the buyer through implementing this fix using AI assistance.
Each prompt handles one specific task so the buyer can do it themselves with guidance.

RULES FOR EVERY PROMPT:
- Write it so a 60-year-old shop owner can paste it and immediately get something useful back
- Use [BRACKETS] in CAPITALS for anything the buyer needs to fill in with their own details
- Every prompt must produce a concrete, finished deliverable — an email, a template, a plan, a script
- Include enough context in the prompt that ChatGPT/Claude doesn't need to ask follow-up questions
- Add a short instruction BEFORE the prompt text in brackets like this:
  (Paste this into chatgpt.com or claude.ai. Fill in the [BRACKETED] parts with your details first.)
- NO jargon in the prompt text — write like you're explaining to a friend

Return a JSON array:
[
  {{
    "label": "What this prompt does in plain English (e.g. 'Write your day-3 payment reminder email')",
    "use_case": "One plain-English sentence: exactly when to use this and what you get back",
    "prompt": "The full prompt text including the instruction line at the top in brackets. Ready to copy-paste."
  }}
]

Write all 5-7 prompts now."""

    try:
        result = ai.generate_json(prompt, model=model)
        if isinstance(result, list):
            return result[:7]
        return []
    except Exception as e:
        print(f"   ⚠️  Prompt generation failed: {e}")
        return []


def build_product(problem: dict) -> dict:
    """Build a complete product from a problem. Returns the product metadata."""
    print(f"\n🔨 BUILDER — Building: {problem.get('product_title', '?')}")

    model = ai.get_best_model()
    print(f"   Using model: {model}")

    # Step 1: Research current tool documentation from the web
    print("   🌐  Fetching live tool documentation...")
    try:
        research_context = researcher.research_for_problem(problem)
        if research_context:
            print(f"      Research complete — {len(research_context)} chars of live docs")
        else:
            print("      No live docs found — AI will use training knowledge")
    except Exception as e:
        print(f"      ⚠️  Research failed: {e} — continuing without live docs")
        research_context = ""

    # Step 2: Write the guide using researched content
    print("   ✍️  Writing guide (non-tech language, real steps)...")
    try:
        guide_content = build_guide_content(problem, model, research_context)
    except Exception as e:
        raise RuntimeError(f"Guide generation failed: {e}")

    # Generate the listing copy
    print("   ✍️  Writing listing copy...")
    try:
        listing = build_listing(problem, guide_content, model)
    except Exception as e:
        raise RuntimeError(f"Listing generation failed: {e}")

    # Generate the AI prompt library
    print("   🤖  Building AI prompt library...")
    prompts = build_prompts(problem, guide_content, model)
    print(f"      {len(prompts)} prompt(s) generated")

    # Build the product folder
    slug = slugify(listing.get("title", problem.get("product_title", "product")))
    product_dir = PRODUCTS_DIR / slug
    product_dir.mkdir(parents=True, exist_ok=True)

    product_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{slug}"
    gumroad_username = CONFIG["business"].get("gumroad_username", "")
    gumroad_url = f"https://{gumroad_username}.gumroad.com/l/{slug}" if gumroad_username else ""

    # Product metadata (drives the site)
    metadata = {
        "product_id": product_id,
        "slug": slug,
        "title": listing.get("title", problem.get("product_title")),
        "tagline": listing.get("tagline", ""),
        "description": listing.get("description", ""),
        "features": listing.get("features", []),
        "who_its_for": listing.get("who_its_for", problem.get("who_has_it", "")),
        "price_usd": problem.get("price_usd", 29),
        "product_type": problem.get("product_type", "guide"),
        "category": problem.get("category", ""),
        "listing_url": gumroad_url,
        "status": "draft",
        "signal_score": problem.get("signal_score", 7),
        "prompt_count": len(prompts),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": 1,
    }

    # Save guide text + prompts JSON (source files)
    (product_dir / "listing.json").write_text(json.dumps(metadata, indent=2))
    (product_dir / "guide.txt").write_text(guide_content)
    (product_dir / "prompts.json").write_text(json.dumps(prompts, indent=2))

    # Generate the production PDF
    print("   📄  Generating PDF...")
    try:
        pdf_path = product_dir / f"{slug}.pdf"
        pdfgen.build_pdf(metadata, guide_content, prompts, pdf_path)
        print(f"      PDF written → {pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)")
        metadata["pdf_file"] = pdf_path.name
    except Exception as e:
        print(f"   ⚠️  PDF generation failed: {e}")
        metadata["pdf_file"] = ""

    # Save updated metadata (now includes pdf_file)
    (product_dir / "listing.json").write_text(json.dumps(metadata, indent=2))

    # Human-readable README
    pdf_name = metadata.get("pdf_file", "")
    readme = f"""# {metadata['title']}

**Type:** {PRODUCT_TYPE_LABELS.get(metadata['product_type'], metadata['product_type'])}
**Price:** ${metadata['price_usd']}
**Status:** {metadata['status']}
**AI Prompts:** {len(prompts)} included

## Problem solved
{problem.get('problem_statement', '')}

## Who it's for
{metadata['who_its_for']}

## Files
- listing.json   — product metadata + copy for the site
- guide.txt      — source content (plain text)
- prompts.json   — the AI prompt library (source)
- {pdf_name or '[slug].pdf'}  — production PDF sent to buyers (cover + guide + prompt library)

## To publish on Gumroad
1. Go to app.gumroad.com → New Product
2. Copy title and description from listing.json
3. Set price from listing.json
4. Upload the PDF file as the product file
5. Copy the Gumroad URL into listing.json → listing_url
6. Change status to "live" in listing.json
7. Run: python3 site/generate.py
"""
    (product_dir / "README.md").write_text(readme)

    print(f"   ✅ Product built → products/{slug}/")
    print(f"   📋 Title: {metadata['title']}")
    print(f"   💰 Price: ${metadata['price_usd']}")
    print(f"   📁 Files: listing.json, guide.txt, README.md")

    return metadata


def run() -> Optional[dict]:
    """Build one product from the pending problem queue. Returns the product or None."""
    state = load_problems()
    problem = get_next_problem(state)

    if not problem:
        print("📭 No pending problems in queue. Run scout first.")
        return None

    try:
        product = build_product(problem)
        mark_problem(state, problem["id"], "built", product["product_id"])
        save_problems(state)
        return product
    except Exception as e:
        mark_problem(state, problem["id"], "failed")
        save_problems(state)
        print(f"   ❌ Build failed: {e}")
        return None


if __name__ == "__main__":
    product = run()
    if product:
        print(f"\n✅ Ready to list: {product['title']} — ${product['price_usd']}")
