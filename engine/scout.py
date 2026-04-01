#!/usr/bin/env python3
"""
scout.py
Finds real business problems that are easily fixable with digital assets.

How it works:
1. Pulls from a seed list of proven high-demand problem categories
2. Uses Ollama to identify specific, concrete problems within each category
3. Scores each problem for: fixability, demand, and how well it fits a digital product
4. Adds validated problems to state/problems.json for the builder to work on
"""

import json
import random
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import ollama_client as ai

STATE_FILE = ROOT / "state" / "problems.json"
CONFIG = json.loads((ROOT / "config.json").read_text())

# Seed categories: real, common, fixable business problems
# Each category is a proven pain point with strong buyer intent
PROBLEM_SEEDS = [
    {
        "category": "payment_collection",
        "theme": "getting paid on time",
        "audience": "freelancers, consultants, small agencies",
        "signal": "clients pay late, awkward follow-up, cash flow gaps"
    },
    {
        "category": "customer_followup",
        "theme": "following up with leads and customers automatically",
        "audience": "small service businesses, gyms, salons, clinics",
        "signal": "leads go cold, no-shows, customers don't come back"
    },
    {
        "category": "online_booking",
        "theme": "taking bookings and appointments without back-and-forth",
        "audience": "coaches, therapists, consultants, service businesses",
        "signal": "booking by phone/email is slow and error-prone"
    },
    {
        "category": "social_proof",
        "theme": "getting more reviews and testimonials automatically",
        "audience": "local businesses, restaurants, trades, clinics",
        "signal": "low review count, competitors have more reviews"
    },
    {
        "category": "lead_capture",
        "theme": "capturing leads from website visitors who don't buy",
        "audience": "ecommerce, service businesses, SaaS",
        "signal": "high traffic but low conversion, no email list"
    },
    {
        "category": "onboarding",
        "theme": "onboarding new clients or customers smoothly",
        "audience": "freelancers, agencies, coaches, SaaS",
        "signal": "messy handoff, lots of back-and-forth at project start"
    },
    {
        "category": "pricing",
        "theme": "pricing services confidently and raising rates",
        "audience": "freelancers, coaches, consultants",
        "signal": "undercharging, scope creep, race to the bottom"
    },
    {
        "category": "proposals",
        "theme": "writing proposals and quotes that win work",
        "audience": "freelancers, agencies, trades, consultants",
        "signal": "losing deals, slow to respond, weak proposals"
    },
    {
        "category": "email_marketing",
        "theme": "sending emails that actually get opened and drive sales",
        "audience": "small ecommerce, local businesses, creators",
        "signal": "email list not converting, low open rates"
    },
    {
        "category": "no_show_prevention",
        "theme": "reducing no-shows and last-minute cancellations",
        "audience": "clinics, salons, coaches, gyms, consultants",
        "signal": "calendar gaps, lost revenue from no-shows"
    },
    {
        "category": "cash_flow",
        "theme": "tracking business income and expenses simply",
        "audience": "solo operators, freelancers, micro-businesses",
        "signal": "no clear picture of profit, surprise tax bills"
    },
    {
        "category": "refunds_complaints",
        "theme": "handling refunds and complaints without losing customers",
        "audience": "ecommerce, service businesses, coaches",
        "signal": "complaints handled badly, chargebacks, bad reviews"
    },
    {
        "category": "ai_content_creation",
        "theme": "using AI to create content faster without losing their voice",
        "audience": "YouTubers, podcasters, newsletter writers, course creators",
        "signal": "content takes too long, can't post consistently, burning out"
    },
    {
        "category": "ai_repurposing",
        "theme": "repurposing one piece of content into many formats using AI",
        "audience": "content creators, coaches, consultants with a YouTube/podcast",
        "signal": "spending hours turning one video into clips, tweets, newsletters"
    },
    {
        "category": "ai_audience_growth",
        "theme": "using AI tools to research what content their audience actually wants",
        "audience": "creators, bloggers, newsletter writers",
        "signal": "creating content that gets ignored, no idea what to post"
    },
    {
        "category": "ai_email_list",
        "theme": "using AI to grow and monetize an email list from existing content",
        "audience": "creators with an audience but no email list or revenue",
        "signal": "followers don't convert to buyers, no direct line to audience"
    },
    {
        "category": "ai_client_content",
        "theme": "using AI to create content for clients faster as a freelancer",
        "audience": "social media managers, copywriters, content agencies",
        "signal": "content production is slow and doesn't scale, low margins"
    },
    {
        "category": "ai_short_form",
        "theme": "using AI to write short-form content that actually drives traffic",
        "audience": "LinkedIn creators, Twitter/X users, TikTok business owners",
        "signal": "posting but getting no traction, inconsistent, wasted time"
    },
]


def load_state() -> dict:
    STATE_FILE.parent.mkdir(exist_ok=True)
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"problems": [], "last_scouted": None, "total_found": 0}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_unbuilt_problems(state: dict) -> list:
    return [p for p in state["problems"] if p["status"] == "pending"]


def search_web_signal(problem_title: str) -> str:
    """
    Search DuckDuckGo for evidence that this problem is real and people are looking for help.
    Returns a short summary of what was found.
    """
    try:
        query = urllib.parse.quote(f"{problem_title} small business how to fix")
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "AIBusiness-Scout/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        abstract = data.get("AbstractText", "")
        related = [r.get("Text", "") for r in data.get("RelatedTopics", [])[:3]]
        combined = abstract + " " + " ".join(related)
        return combined[:500] if combined.strip() else "No web signal found"
    except Exception:
        return "Web search unavailable — using AI signal scoring only"


def scout_problems(n: int = 3) -> list[dict]:
    """
    Use Ollama to identify specific, concrete, fixable business problems.
    Returns a list of scored problem objects.
    """
    seed = random.sample(PROBLEM_SEEDS, min(n, len(PROBLEM_SEEDS)))
    problems = []

    for item in seed:
        print(f"  🔍 Scouting: {item['theme']}...")

        prompt = f"""You are a business analyst finding specific, fixable problems that small businesses have.

Category: {item['category']}
Theme: {item['theme']}
Typical audience: {item['audience']}
Common signals: {item['signal']}

Identify ONE specific, concrete problem that many small businesses in this space have.
The problem must be:
- Easily fixable with a digital guide, template, or checklist (no custom software needed)
- Solvable in under 2 hours with the right instructions
- Something a business owner would pay $19-$49 to fix today

Return a JSON object with these fields:
{{
  "title": "Short problem title (under 10 words)",
  "problem_statement": "Exactly what's going wrong for the business (2-3 sentences)",
  "who_has_it": "Specific type of business that has this problem",
  "why_fixable": "Why this can be fixed with a digital guide/template",
  "product_type": "One of: guide, template, checklist, blueprint, swipe_file",
  "product_title": "Title of the digital product that fixes this (punchy, benefit-focused)",
  "price_usd": 19 or 29 or 49,
  "signal_score": a number 1-10 for how strong buyer demand is,
  "fix_time_hours": estimated hours to implement the fix
}}"""

        try:
            problem = ai.generate_json(prompt)
            problem["category"] = item["category"]
            problem["status"] = "pending"
            problem["id"] = f"PROB-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{item['category']}"
            problem["found_at"] = datetime.now().isoformat()
            problems.append(problem)
            print(f"     Found: {problem.get('product_title', '?')} (signal: {problem.get('signal_score', '?')}/10)")
        except Exception as e:
            print(f"     ⚠️  Skipped {item['category']}: {e}")
            continue

    return problems


def run(n: int = 3) -> list[dict]:
    """Main scout function. Find n new problems and add to state."""
    print(f"\n🔍 SCOUT — Finding {n} fixable business problems...")

    state = load_state()
    pending = get_unbuilt_problems(state)

    if len(pending) >= 5:
        print(f"   Already have {len(pending)} pending problems — skipping scout this cycle")
        return pending

    new_problems = scout_problems(n)

    # Filter by minimum signal score
    min_score = CONFIG["scout"].get("min_signal_score", 6)
    qualified = [p for p in new_problems if p.get("signal_score", 0) >= min_score]
    low_signal = [p for p in new_problems if p.get("signal_score", 0) < min_score]

    if low_signal:
        print(f"   Filtered out {len(low_signal)} low-signal problem(s) (score < {min_score})")

    state["problems"].extend(qualified)
    state["last_scouted"] = datetime.now().isoformat()
    state["total_found"] = state.get("total_found", 0) + len(qualified)
    save_state(state)

    print(f"   ✅ Added {len(qualified)} qualified problem(s) to queue")
    return qualified


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    found = run(n)
    print(f"\nProblems queued for building:")
    for p in found:
        print(f"  • [{p.get('signal_score')}/10] {p.get('product_title')} — ${p.get('price_usd')}")
