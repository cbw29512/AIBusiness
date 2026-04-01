#!/usr/bin/env python3
"""
generate.py
Reads all product listings and generates index.html.
Run automatically by the main loop after each build cycle.

Usage: python3 site/generate.py
"""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRODUCTS_DIR = ROOT / "products"
OUTPUT = ROOT / "index.html"
CONFIG = json.loads((ROOT / "config.json").read_text())
BIZ = CONFIG["business"]

THEMES = [
    {"card": "amber",  "badge": "badge-amber",  "btn": "btn-amber"},
    {"card": "green",  "badge": "badge-green",  "btn": "btn-green"},
    {"card": "blue",   "badge": "badge-blue",   "btn": "btn-blue"},
    {"card": "purple", "badge": "badge-purple", "btn": "btn-purple"},
]

TYPE_LABELS = {
    "guide":      "Step-by-Step Guide",
    "template":   "Ready-to-Use Template",
    "checklist":  "Action Checklist",
    "blueprint":  "Implementation Blueprint",
    "swipe_file": "Swipe File",
}

TYPE_ICONS = {
    "guide":      "📋",
    "template":   "📊",
    "checklist":  "✅",
    "blueprint":  "🗺️",
    "swipe_file": "📁",
}

CATEGORY_ICONS = {
    "ai_content_creation": "🤖",
    "ai_repurposing":      "♻️",
    "ai_audience_growth":  "📈",
    "ai_email_list":       "📬",
    "ai_client_content":   "✍️",
    "ai_short_form":       "⚡",
    "payment_collection":  "💸",
    "customer_followup":   "🔔",
    "online_booking":      "📅",
    "social_proof":        "⭐",
    "lead_capture":        "🎯",
    "onboarding":          "🚀",
    "pricing":             "💰",
    "proposals":           "📝",
    "email_marketing":     "📧",
    "no_show_prevention":  "🚫",
    "cash_flow":           "📊",
    "refunds_complaints":  "🛡️",
}


def load_products() -> list[dict]:
    products = []
    if not PRODUCTS_DIR.exists():
        return products

    for folder in sorted(PRODUCTS_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        listing_file = folder / "listing.json"
        if not listing_file.exists():
            continue
        try:
            data = json.loads(listing_file.read_text())
        except Exception:
            continue
        if data.get("status") == "retired":
            continue
        products.append(data)

    return products


def product_card(product: dict, theme: dict, is_new: bool = False) -> str:
    ptype = product.get("product_type", "guide")
    cat = product.get("category", "")
    icon = CATEGORY_ICONS.get(cat) or TYPE_ICONS.get(ptype, "📦")
    label = TYPE_LABELS.get(ptype, "Digital Product")
    price = product.get("price_usd", 29)
    url = product.get("listing_url", "")
    title = product.get("title", "Untitled")
    desc = product.get("description", "")
    features = product.get("features", [])[:5]
    tagline = product.get("tagline", "")

    btn_url = url if url else "#"
    btn_text = "Get Instant Access →" if url else "Coming Soon"
    btn_disabled = "" if url else ' style="opacity:0.5;pointer-events:none;cursor:default;"'
    prompt_count = product.get("prompt_count", 0)
    prompt_chip = (f'<span class="prompt-chip">🤖 {prompt_count} AI prompts included</span>'
                   if prompt_count else '')

    new_badge = '<span class="new-badge">NEW</span>' if is_new else ""
    features_html = "\n".join(f'            <li>{f}</li>' for f in features)

    return f"""
      <div class="card {theme['card']}">
        {new_badge}
        <div class="card-badge {theme['badge']}">{label}</div>
        <div class="card-icon">{icon}</div>
        <h3>{title}</h3>
        <p class="card-tagline">{tagline}</p>
        <p class="card-desc">{desc[:200]}{"..." if len(desc) > 200 else ""}</p>
        <ul class="card-features">
{features_html}
        </ul>
        {prompt_chip}
        <div class="card-footer">
          <div class="card-price">${price} <span>one-time</span></div>
          <a href="{btn_url}" class="btn {theme['btn']}"{btn_disabled} target="_blank" rel="noopener">{btn_text}</a>
        </div>
      </div>"""


def build_html(products: list[dict]) -> str:
    now = datetime.now()
    updated = now.strftime("%B %d, %Y at %I:%M %p")
    product_count = len(products)
    ai_count = sum(1 for p in products if "ai_" in p.get("category", ""))

    # Mark products from last 72 hours as NEW
    cards_html = ""
    for i, product in enumerate(products):
        theme = THEMES[i % len(THEMES)]
        try:
            created = datetime.fromisoformat(product.get("created_at", ""))
            is_new = (now - created).total_seconds() < 72 * 3600
        except Exception:
            is_new = False
        cards_html += product_card(product, theme, is_new)

    if not cards_html:
        cards_html = '<p class="empty-state">First products building now — check back in a few minutes.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{BIZ['site_title']}</title>
  <meta name="description" content="{BIZ['site_tagline']}" />
  <meta property="og:title" content="{BIZ['site_title']}" />
  <meta property="og:description" content="{BIZ['site_tagline']}" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --black:#0a0a0a; --dark:#111827; --mid:#1f2937; --border:#2d3748;
      --text:#e5e7eb; --muted:#9ca3af;
      --amber:#f59e0b; --amber-dark:#d97706;
      --green:#10b981; --blue:#3b82f6; --purple:#8b5cf6;
    }}
    html {{ scroll-behavior: smooth; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: var(--black); color: var(--text); line-height: 1.6; }}

    /* NAV */
    nav {{ position:sticky; top:0; z-index:100; background:rgba(10,10,10,0.96); backdrop-filter:blur(12px); border-bottom:1px solid var(--border); padding:0.9rem 2rem; display:flex; align-items:center; justify-content:space-between; gap:1rem; }}
    .nav-logo {{ font-weight:900; font-size:1rem; color:var(--amber); letter-spacing:-0.3px; }}
    .nav-live {{ display:flex; align-items:center; gap:0.5rem; font-size:0.78rem; color:var(--muted); }}
    .live-dot {{ width:7px; height:7px; border-radius:50%; background:var(--green); animation:pulse 2s infinite; }}
    @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.4}} }}
    .nav-right {{ font-size:0.8rem; color:var(--muted); }}

    /* HERO */
    .hero {{ max-width:800px; margin:0 auto; padding:5rem 2rem 3.5rem; text-align:center; }}
    .hero-eyebrow {{ display:inline-block; background:rgba(245,158,11,0.12); border:1px solid rgba(245,158,11,0.3); color:var(--amber); font-size:0.75rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding:0.35rem 1rem; border-radius:100px; margin-bottom:1.5rem; }}
    .hero h1 {{ font-size:clamp(2rem,5vw,3.5rem); font-weight:900; line-height:1.1; letter-spacing:-1.5px; margin-bottom:1.2rem; }}
    .hero h1 span {{ background:linear-gradient(135deg,var(--amber),#f97316); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }}
    .hero-sub {{ font-size:1.1rem; color:var(--muted); max-width:560px; margin:0 auto 1.5rem; line-height:1.7; }}
    .hero-cta {{ display:inline-block; background:var(--amber); color:var(--black); font-weight:800; font-size:0.95rem; padding:0.85rem 2rem; border-radius:8px; text-decoration:none; transition:background 0.2s,transform 0.1s; margin-bottom:2rem; }}
    .hero-cta:hover {{ background:var(--amber-dark); transform:translateY(-1px); }}

    /* LIVE UPDATE BANNER */
    .live-banner {{ background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2); border-radius:12px; padding:1rem 1.5rem; max-width:700px; margin:0 auto 3rem; display:flex; align-items:flex-start; gap:1rem; text-align:left; }}
    .live-banner-icon {{ font-size:1.4rem; flex-shrink:0; margin-top:2px; }}
    .live-banner h4 {{ font-size:0.9rem; font-weight:700; color:var(--green); margin-bottom:0.3rem; }}
    .live-banner p {{ font-size:0.83rem; color:var(--muted); line-height:1.5; }}

    /* STATS */
    .stats-row {{ display:flex; justify-content:center; gap:2.5rem; padding-top:2.5rem; border-top:1px solid var(--border); flex-wrap:wrap; }}
    .stat {{ text-align:center; }}
    .stat-num {{ font-size:1.8rem; font-weight:900; color:var(--amber); }}
    .stat-lbl {{ font-size:0.8rem; color:var(--muted); margin-top:0.2rem; }}

    /* SECTIONS */
    section {{ padding:4.5rem 2rem; }}
    .section-inner {{ max-width:1100px; margin:0 auto; }}
    .section-label {{ font-size:0.75rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--amber); margin-bottom:0.6rem; }}
    .section-title {{ font-size:clamp(1.6rem,3vw,2.4rem); font-weight:800; letter-spacing:-0.8px; margin-bottom:0.8rem; }}
    .section-sub {{ color:var(--muted); font-size:1rem; max-width:500px; margin-bottom:2.5rem; line-height:1.65; }}

    /* PRODUCTS */
    .products-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:1.5rem; }}
    .card {{ background:var(--dark); border:1px solid var(--border); border-radius:14px; padding:1.75rem; display:flex; flex-direction:column; transition:border-color 0.2s,transform 0.2s; position:relative; overflow:hidden; }}
    .card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:3px; }}
    .card.amber::before {{ background:linear-gradient(90deg,var(--amber),#f97316); }}
    .card.green::before  {{ background:linear-gradient(90deg,var(--green),#06b6d4); }}
    .card.blue::before   {{ background:linear-gradient(90deg,var(--blue),var(--purple)); }}
    .card.purple::before {{ background:linear-gradient(90deg,var(--purple),#ec4899); }}
    .card:hover {{ border-color:rgba(245,158,11,0.35); transform:translateY(-2px); }}
    .new-badge {{ position:absolute; top:1rem; right:1rem; background:var(--green); color:var(--black); font-size:0.65rem; font-weight:800; letter-spacing:1px; padding:0.2rem 0.5rem; border-radius:4px; }}
    .prompt-chip {{ display:inline-block; background:rgba(139,92,246,0.12); border:1px solid rgba(139,92,246,0.25); color:var(--purple); font-size:0.75rem; font-weight:600; padding:0.3rem 0.7rem; border-radius:100px; margin-bottom:1rem; }}
    .card-badge {{ display:inline-block; font-size:0.68rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; padding:0.2rem 0.65rem; border-radius:100px; margin-bottom:1rem; width:fit-content; }}
    .badge-amber {{ background:rgba(245,158,11,0.12); color:var(--amber); }}
    .badge-green {{ background:rgba(16,185,129,0.12); color:var(--green); }}
    .badge-blue  {{ background:rgba(59,130,246,0.12); color:var(--blue); }}
    .badge-purple {{ background:rgba(139,92,246,0.12); color:var(--purple); }}
    .card-icon {{ font-size:2rem; margin-bottom:0.8rem; }}
    .card h3 {{ font-size:1.1rem; font-weight:800; margin-bottom:0.4rem; line-height:1.3; }}
    .card-tagline {{ font-size:0.88rem; color:var(--amber); margin-bottom:0.6rem; font-weight:500; font-style:italic; }}
    .card-desc {{ color:var(--muted); font-size:0.88rem; line-height:1.6; margin-bottom:1.2rem; flex-grow:1; }}
    .card-features {{ list-style:none; margin-bottom:1.5rem; }}
    .card-features li {{ font-size:0.83rem; color:var(--muted); padding:0.2rem 0; display:flex; align-items:flex-start; gap:0.45rem; }}
    .card-features li::before {{ content:'✓'; color:var(--green); font-weight:700; flex-shrink:0; }}
    .card-footer {{ display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-top:auto; padding-top:1.25rem; border-top:1px solid var(--border); }}
    .card-price {{ font-size:1.5rem; font-weight:900; letter-spacing:-0.8px; }}
    .card-price span {{ font-size:0.85rem; font-weight:400; color:var(--muted); }}
    .btn {{ display:inline-block; font-weight:700; font-size:0.85rem; padding:0.65rem 1.3rem; border-radius:7px; text-decoration:none; text-align:center; transition:all 0.2s; border:none; white-space:nowrap; cursor:pointer; }}
    .btn-amber  {{ background:var(--amber);  color:var(--black); }} .btn-amber:hover  {{ background:var(--amber-dark); transform:translateY(-1px); }}
    .btn-green  {{ background:var(--green);  color:var(--black); }} .btn-green:hover  {{ background:#059669; transform:translateY(-1px); }}
    .btn-blue   {{ background:var(--blue);   color:#fff; }}         .btn-blue:hover   {{ background:#2563eb; transform:translateY(-1px); }}
    .btn-purple {{ background:var(--purple); color:#fff; }}         .btn-purple:hover {{ background:#7c3aed; transform:translateY(-1px); }}

    /* CREATOR SECTION */
    .creator-banner {{ background:linear-gradient(135deg,#1a1040,#0f172a); border:1px solid rgba(139,92,246,0.3); border-radius:16px; padding:2.5rem; position:relative; overflow:hidden; }}
    .creator-banner::before {{ content:'🤖'; position:absolute; right:2rem; top:50%; transform:translateY(-50%); font-size:5rem; opacity:0.1; }}
    .creator-eyebrow {{ font-size:0.7rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--purple); margin-bottom:0.6rem; }}
    .creator-banner h2 {{ font-size:1.6rem; font-weight:800; letter-spacing:-0.5px; margin-bottom:0.8rem; }}
    .creator-banner p {{ color:var(--muted); font-size:0.93rem; line-height:1.65; max-width:480px; }}
    .creator-tags {{ display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:1.2rem; }}
    .creator-tag {{ background:rgba(139,92,246,0.12); border:1px solid rgba(139,92,246,0.25); color:var(--purple); font-size:0.75rem; font-weight:600; padding:0.3rem 0.7rem; border-radius:100px; }}

    /* HOW IT WORKS */
    .steps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:2rem; margin-top:2.5rem; }}
    .step {{ display:flex; flex-direction:column; gap:0.6rem; }}
    .step-num {{ width:36px; height:36px; border-radius:9px; background:rgba(245,158,11,0.12); border:1px solid rgba(245,158,11,0.3); color:var(--amber); font-weight:800; font-size:0.9rem; display:flex; align-items:center; justify-content:center; }}
    .step h4 {{ font-size:0.9rem; font-weight:700; }}
    .step p {{ font-size:0.83rem; color:var(--muted); line-height:1.6; }}

    /* GUARANTEE */
    .guarantee {{ background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.18); border-radius:14px; padding:2rem; display:flex; gap:1.5rem; align-items:flex-start; flex-wrap:wrap; margin-top:2.5rem; }}
    .guarantee-icon {{ font-size:2.5rem; flex-shrink:0; }}
    .guarantee h3 {{ font-size:1rem; font-weight:800; margin-bottom:0.4rem; }}
    .guarantee p {{ color:var(--muted); font-size:0.87rem; line-height:1.6; }}

    /* FAQ */
    .faq {{ margin-top:2.5rem; }}
    .faq-item {{ border-bottom:1px solid var(--border); padding:1.25rem 0; }}
    .faq-item:first-child {{ border-top:1px solid var(--border); }}
    .faq-q {{ font-weight:700; font-size:0.93rem; margin-bottom:0.5rem; }}
    .faq-a {{ color:var(--muted); font-size:0.87rem; line-height:1.65; }}

    .divider {{ border:none; border-top:1px solid var(--border); margin:0; }}
    footer {{ border-top:1px solid var(--border); padding:2.5rem 2rem; text-align:center; color:var(--muted); font-size:0.82rem; }}
    .empty-state {{ color:var(--muted); text-align:center; padding:4rem 0; font-size:0.95rem; }}

    @media (max-width:640px) {{
      nav {{ padding:0.9rem 1rem; }} .nav-right {{ display:none; }}
      .hero {{ padding:3.5rem 1.25rem 2.5rem; }} section {{ padding:3rem 1.25rem; }}
      .stats-row {{ gap:1.5rem; }} .live-banner {{ flex-direction:column; gap:0.5rem; }}
    }}
  </style>
</head>
<body>

<nav>
  <div class="nav-logo">AIBusiness</div>
  <div class="nav-live">
    <div class="live-dot"></div>
    AI updating constantly
  </div>
  <div class="nav-right">Last updated: {updated}</div>
</nav>

<div class="hero">
  <div class="hero-eyebrow">AI-researched · Constantly updated · Real fixes</div>
  <h1>Real problems.<br /><span>AI-built solutions.</span></h1>
  <p class="hero-sub">{BIZ['site_tagline']}. New fixes added automatically as our AI finds them.</p>
  <a href="#products" class="hero-cta">See What We've Found →</a>

  <div class="live-banner">
    <div class="live-banner-icon">🔄</div>
    <div>
      <h4>Living updates — this page refreshes automatically</h4>
      <p>Our AI scans businesses continuously for real, fixable problems. Every guide and template here was built from actual evidence of demand — not guesswork. New solutions appear here as they're built. Bookmark this page and check back regularly.</p>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat"><div class="stat-num">{product_count}</div><div class="stat-lbl">solutions available now</div></div>
    <div class="stat"><div class="stat-num">{ai_count}</div><div class="stat-lbl">AI creator tools</div></div>
    <div class="stat"><div class="stat-num">&lt;2hrs</div><div class="stat-lbl">average implementation time</div></div>
    <div class="stat"><div class="stat-num">$0</div><div class="stat-lbl">to start (all free tools)</div></div>
  </div>
</div>

<hr class="divider" />

<!-- CREATOR SPOTLIGHT -->
<section style="background:var(--dark);">
  <div class="section-inner">
    <div class="creator-banner">
      <div class="creator-eyebrow">Creator Niche</div>
      <h2>AI tools for content creators who mean business</h2>
      <p>We track how AI tools for content creation, repurposing, and audience growth are changing — and build guides that stay current with the latest techniques. If you create content, our AI-specific guides are updated whenever the tools or best practices shift.</p>
      <div class="creator-tags">
        <span class="creator-tag">AI Content Creation</span>
        <span class="creator-tag">Repurposing Workflows</span>
        <span class="creator-tag">Audience Research</span>
        <span class="creator-tag">Email Monetization</span>
        <span class="creator-tag">Short-form Strategy</span>
        <span class="creator-tag">Client Content at Scale</span>
      </div>
    </div>
  </div>
</section>

<hr class="divider" />

<section id="products">
  <div class="section-inner">
    <div class="section-label">Solutions Library</div>
    <h2 class="section-title">AI-researched. Human-readable. Actually works.</h2>
    <p class="section-sub">Every fix here was built because our AI found real evidence that businesses are struggling with it right now.</p>
    <div class="products-grid">
{cards_html}
    </div>
  </div>
</section>

<hr class="divider" />

<section>
  <div class="section-inner">
    <div class="section-label">How It Works</div>
    <h2 class="section-title">From real problem to working fix</h2>
    <div class="steps">
      <div class="step"><div class="step-num">1</div><h4>AI finds a real problem</h4><p>Our AI scans businesses for common, high-signal pain points with documented demand and easy fixes.</p></div>
      <div class="step"><div class="step-num">2</div><h4>Builds the solution</h4><p>A complete guide, template, or blueprint is generated — step-by-step, tool-specific, copy-paste ready.</p></div>
      <div class="step"><div class="step-num">3</div><h4>You buy and implement</h4><p>Instant download via Gumroad. Follow the steps. Most fixes take under 2 hours to implement.</p></div>
      <div class="step"><div class="step-num">4</div><h4>AI updates when needed</h4><p>If tools change or better methods emerge, AI creator guides get updated. You get living documentation, not a static PDF.</p></div>
    </div>
    <div class="guarantee">
      <div class="guarantee-icon">🛡️</div>
      <div>
        <h3>30-Day Money-Back Guarantee</h3>
        <p>Follow the steps and it doesn't work? Email us within 30 days for a full refund. No questions, no forms. These are built from real problems — if the fix doesn't work for you, you don't pay.</p>
      </div>
    </div>
  </div>
</section>

<hr class="divider" />

<section id="faq" style="background:var(--dark);">
  <div class="section-inner">
    <div class="section-label">FAQ</div>
    <h2 class="section-title">Questions answered</h2>
    <div class="faq">
      <div class="faq-item"><div class="faq-q">How is this different from a regular digital product store?</div><div class="faq-a">Every product here was built because AI found evidence that real businesses have this problem right now. We don't guess what to sell — we find the problem first, then build the fix. New products appear regularly as new problems are found.</div></div>
      <div class="faq-item"><div class="faq-q">What does "constantly updated" mean for the AI creator guides?</div><div class="faq-a">AI tools change fast. When our system detects that a guide references outdated tools or techniques, it rebuilds the guide with current information. Buyers of AI creator guides get access to the most recent version.</div></div>
      <div class="faq-item"><div class="faq-q">Do I need to be technical?</div><div class="faq-a">No. Every guide is written for the business owner, not a developer. We recommend specific free tools and show you exactly how to use them. If you can follow a recipe, you can implement these fixes.</div></div>
      <div class="faq-item"><div class="faq-q">How is the product delivered?</div><div class="faq-a">Instantly via Gumroad after purchase. You get a download link by email. No account needed — just click and download.</div></div>
      <div class="faq-item"><div class="faq-q">Why is the price so low?</div><div class="faq-a">Because AI builds these efficiently. We pass that on. A $29 fix that saves you 3 hours a week is a 10x return in the first month alone.</div></div>
    </div>
  </div>
</section>

<footer>
  <p>© {datetime.now().year} AIBusiness — AI-researched solutions to real business problems.</p>
  <p style="margin-top:0.5rem;">Questions? <a href="mailto:{BIZ['contact_email']}" style="color:var(--amber);text-decoration:none;">{BIZ['contact_email']}</a></p>
  <p style="margin-top:0.75rem; font-size:0.72rem; color:#374151;">Last updated by AI: {updated} · {product_count} solution(s) in library</p>
</footer>

</body>
</html>"""


def main():
    print("⚙️  Generating site...")
    products = load_products()
    print(f"   {len(products)} active product(s)")
    html = build_html(products)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"✅ index.html written → {OUTPUT}")


if __name__ == "__main__":
    main()
