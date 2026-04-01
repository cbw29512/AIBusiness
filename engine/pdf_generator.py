#!/usr/bin/env python3
"""
pdf_generator.py
Generates a professional, production-ready PDF for each AIBusiness product.

Each PDF contains:
  1. Cover page — title, tagline, what's inside
  2. The Problem — what's going wrong and why it matters
  3. What You'll Have After — concrete outcomes
  4. Step-by-Step Fix — numbered, specific, actionable
  5. Templates & Scripts — copy-paste ready
  6. AI Prompt Library — tested prompts for ChatGPT/Claude so buyers can DIY with guidance
  7. Quick Win — the single most important first step
"""

import re
import textwrap
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import KeepTogether

# ── Brand colours ─────────────────────────────────────────────────────────────
AMBER  = colors.HexColor("#f59e0b")
DARK   = colors.HexColor("#111827")
MID    = colors.HexColor("#1f2937")
MUTED  = colors.HexColor("#6b7280")
GREEN  = colors.HexColor("#10b981")
BLUE   = colors.HexColor("#3b82f6")
PURPLE = colors.HexColor("#8b5cf6")
WHITE  = colors.white
BLACK  = colors.HexColor("#0a0a0a")
LIGHT_AMBER = colors.HexColor("#fef3c7")
LIGHT_GREEN = colors.HexColor("#d1fae5")
LIGHT_BLUE  = colors.HexColor("#dbeafe")
LIGHT_PURPLE = colors.HexColor("#ede9fe")


# ── Style sheet ───────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "cover_title": s("cover_title",
            fontName="Helvetica-Bold", fontSize=32, leading=38,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=12),

        "cover_tagline": s("cover_tagline",
            fontName="Helvetica", fontSize=14, leading=20,
            textColor=colors.HexColor("#d1d5db"), alignment=TA_CENTER, spaceAfter=6),

        "cover_meta": s("cover_meta",
            fontName="Helvetica", fontSize=10,
            textColor=colors.HexColor("#9ca3af"), alignment=TA_CENTER),

        "section_label": s("section_label",
            fontName="Helvetica-Bold", fontSize=8, leading=12,
            textColor=AMBER, spaceBefore=24, spaceAfter=4,
            letterSpacing=1.5),

        "h1": s("h1",
            fontName="Helvetica-Bold", fontSize=22, leading=27,
            textColor=DARK, spaceBefore=6, spaceAfter=10),

        "h2": s("h2",
            fontName="Helvetica-Bold", fontSize=15, leading=20,
            textColor=DARK, spaceBefore=18, spaceAfter=6),

        "h3": s("h3",
            fontName="Helvetica-Bold", fontSize=12, leading=16,
            textColor=DARK, spaceBefore=12, spaceAfter=4),

        "body": s("body",
            fontName="Helvetica", fontSize=10.5, leading=16,
            textColor=colors.HexColor("#374151"), spaceAfter=8),

        "body_muted": s("body_muted",
            fontName="Helvetica", fontSize=10, leading=15,
            textColor=MUTED, spaceAfter=6),

        "step_num": s("step_num",
            fontName="Helvetica-Bold", fontSize=10,
            textColor=AMBER),

        "step_title": s("step_title",
            fontName="Helvetica-Bold", fontSize=11, leading=15,
            textColor=DARK, spaceAfter=3),

        "step_body": s("step_body",
            fontName="Helvetica", fontSize=10, leading=15,
            textColor=colors.HexColor("#374151"), spaceAfter=8, leftIndent=20),

        "bullet": s("bullet",
            fontName="Helvetica", fontSize=10.5, leading=16,
            textColor=colors.HexColor("#374151"), spaceAfter=4,
            leftIndent=16, bulletIndent=0),

        "prompt_label": s("prompt_label",
            fontName="Helvetica-Bold", fontSize=9, leading=13,
            textColor=PURPLE, spaceAfter=3, spaceBefore=12),

        "prompt_use": s("prompt_use",
            fontName="Helvetica-Oblique", fontSize=9, leading=13,
            textColor=MUTED, spaceAfter=4),

        "prompt_text": s("prompt_text",
            fontName="Courier", fontSize=8.5, leading=13,
            textColor=colors.HexColor("#1e1b4b"),
            backColor=colors.HexColor("#f5f3ff"),
            spaceAfter=8, leftIndent=10, rightIndent=10,
            borderPad=6),

        "tip_box": s("tip_box",
            fontName="Helvetica-Oblique", fontSize=10, leading=15,
            textColor=colors.HexColor("#065f46"),
            backColor=LIGHT_GREEN,
            spaceAfter=10, borderPad=8),

        "footer": s("footer",
            fontName="Helvetica", fontSize=8,
            textColor=MUTED, alignment=TA_CENTER),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────
def hr(color=colors.HexColor("#e5e7eb"), thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=12, spaceBefore=4)


def section_header(label: str, title: str, styles: dict):
    return [
        Paragraph(label.upper(), styles["section_label"]),
        Paragraph(title, styles["h1"]),
        hr(),
    ]


def outcome_table(outcomes: list[str], styles: dict):
    """Render a 2-column outcome/checklist table."""
    rows = []
    for i in range(0, len(outcomes), 2):
        left = f"<font color='#10b981'>&#10003;</font>  {outcomes[i]}"
        right = f"<font color='#10b981'>&#10003;</font>  {outcomes[i+1]}" if i+1 < len(outcomes) else ""
        rows.append([
            Paragraph(left, styles["body"]),
            Paragraph(right, styles["body"]),
        ])
    t = Table(rows, colWidths=[3.3*inch, 3.3*inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [LIGHT_GREEN, WHITE]),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [4,4,4,4]),
    ]))
    return t


def prompt_box(label: str, use_case: str, prompt_text: str, styles: dict):
    """Render a single prompt card."""
    cleaned = prompt_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return KeepTogether([
        Paragraph(f"PROMPT: {label}", styles["prompt_label"]),
        Paragraph(f"When to use: {use_case}", styles["prompt_use"]),
        Paragraph(cleaned, styles["prompt_text"]),
    ])


# ── Section parsers ───────────────────────────────────────────────────────────
def parse_steps(guide_text: str) -> list[dict]:
    """Extract numbered steps from guide text."""
    steps = []
    lines = guide_text.split("\n")
    current = None

    for line in lines:
        stripped = line.strip()
        # Match patterns like "1.", "Step 1:", "1)"
        m = re.match(r'^(?:Step\s+)?(\d+)[.):]\s*(.+)', stripped, re.IGNORECASE)
        if m:
            if current:
                steps.append(current)
            current = {"num": m.group(1), "title": m.group(2), "body": []}
        elif current and stripped and not stripped.startswith("===") and not stripped.startswith("---"):
            current["body"].append(stripped)

    if current:
        steps.append(current)

    return steps[:12]  # cap at 12 steps


def parse_section(guide_text: str, keywords: list[str]) -> str:
    """Extract a section from guide text by keyword header."""
    lines = guide_text.split("\n")
    in_section = False
    result = []

    for line in lines:
        stripped = line.strip()
        upper = stripped.upper()

        if any(kw.upper() in upper for kw in keywords):
            in_section = True
            continue

        if in_section:
            # Stop at next major header
            if (stripped.startswith("===") or stripped.startswith("---") or
                    (stripped.isupper() and len(stripped) > 5 and stripped == stripped.upper())):
                if result:
                    break
                continue
            if stripped:
                result.append(stripped)

    return " ".join(result[:6])


def parse_bullets(guide_text: str, keyword: str) -> list[str]:
    """Extract bullet list items after a keyword header."""
    lines = guide_text.split("\n")
    in_section = False
    bullets = []

    for line in lines:
        stripped = line.strip()
        if keyword.upper() in stripped.upper():
            in_section = True
            continue
        if in_section:
            if stripped.startswith(("- ", "• ", "* ")):
                bullets.append(stripped.lstrip("-•* ").strip())
            elif stripped.startswith(("===", "---")) and bullets:
                break

    return bullets[:8]


# ── Cover page ────────────────────────────────────────────────────────────────
def cover_page(product: dict, styles: dict) -> list:
    story = []

    # Version + date info
    version = product.get("version", 1)
    last_updated = product.get("last_updated") or product.get("created_at", "")
    try:
        updated_date = datetime.fromisoformat(last_updated).strftime("%B %Y")
    except (ValueError, TypeError):
        updated_date = datetime.now().strftime("%B %Y")

    version_label = f"v{version} · Updated {updated_date}" if version > 1 else updated_date

    # Dark header bar (faked with table)
    header_data = [[Paragraph(
        f"<font color='#f59e0b'>AIBusiness</font> &nbsp;·&nbsp; "
        f"<font color='#9ca3af'>{version_label}</font>",
        ParagraphStyle("hdr", fontName="Helvetica", fontSize=9, textColor=WHITE)
    )]]
    header = Table(header_data, colWidths=[6.8*inch])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
    ]))
    story.append(header)
    story.append(Spacer(1, 0.6*inch))

    # Badge
    ptype = product.get("product_type", "guide").replace("_", " ").title()
    badge_data = [[Paragraph(ptype.upper(),
        ParagraphStyle("badge", fontName="Helvetica-Bold", fontSize=8,
                       textColor=AMBER, alignment=TA_CENTER))]]
    badge = Table(badge_data, colWidths=[1.8*inch])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1c1407")),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("BOX", (0,0), (-1,-1), 0.5, AMBER),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [6,6,6,6]),
    ]))

    # Center badge
    badge_row = Table([[badge]], colWidths=[6.8*inch])
    badge_row.setStyle(TableStyle([("ALIGN", (0,0), (-1,-1), "CENTER")]))
    story.append(badge_row)
    story.append(Spacer(1, 0.3*inch))

    # Title box
    title_data = [[Paragraph(product["title"], styles["cover_title"])]]
    title_box = Table(title_data, colWidths=[6.8*inch])
    title_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK),
        ("TOPPADDING", (0,0), (-1,-1), 30),
        ("BOTTOMPADDING", (0,0), (-1,-1), 24),
        ("LEFTPADDING", (0,0), (-1,-1), 24),
        ("RIGHTPADDING", (0,0), (-1,-1), 24),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [10,10,10,10]),
    ]))
    story.append(title_box)
    story.append(Spacer(1, 0.25*inch))

    # Tagline
    if product.get("tagline"):
        story.append(Paragraph(product["tagline"],
            ParagraphStyle("tl", fontName="Helvetica-Oblique", fontSize=13, leading=19,
                           textColor=MUTED, alignment=TA_CENTER, spaceAfter=8)))

    story.append(Spacer(1, 0.3*inch))

    # What's inside chips
    inside_items = [
        "Step-by-step fix",
        "Copy-paste templates",
        "Free tool recommendations",
        "Tested AI prompts",
        "Living updates included",
    ]
    chips = [[Paragraph(item,
        ParagraphStyle("chip", fontName="Helvetica", fontSize=8.5,
                       textColor=DARK, alignment=TA_CENTER))
              for item in inside_items]]
    chip_table = Table(chips, colWidths=[1.36*inch]*5)
    chip_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_AMBER),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("BOX", (0,0), (-1,-1), 0.5, AMBER),
        ("INNERGRID", (0,0), (-1,-1), 0.3, AMBER),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [4,4,4,4]),
    ]))
    story.append(chip_table)

    story.append(Spacer(1, 0.5*inch))

    # Price + guarantee row
    price_str = f"${product.get('price_usd', 29)}"
    meta_data = [[
        Paragraph(price_str,
            ParagraphStyle("price", fontName="Helvetica-Bold", fontSize=18,
                           textColor=AMBER, alignment=TA_CENTER)),
        Paragraph("one-time",
            ParagraphStyle("ot", fontName="Helvetica", fontSize=9,
                           textColor=MUTED, alignment=TA_CENTER)),
        Paragraph("30-day money-back guarantee",
            ParagraphStyle("guar", fontName="Helvetica", fontSize=9,
                           textColor=GREEN, alignment=TA_CENTER)),
    ]]
    meta_table = Table(meta_data, colWidths=[1.5*inch, 1.5*inch, 3.8*inch])
    meta_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 0.6*inch))
    story.append(hr(AMBER, 1))

    footer_txt = (
        f"Generated by AIBusiness AI · {datetime.now().strftime('%B %d, %Y')} · "
        "This document is updated when tools or best practices change."
    )
    story.append(Paragraph(footer_txt, styles["footer"]))

    story.append(PageBreak())
    return story


# ── Main PDF builder ──────────────────────────────────────────────────────────
def build_pdf(product: dict, guide_text: str, prompts: list[dict], output_path: Path) -> Path:
    """
    Build the full product PDF.

    Args:
        product:     listing.json dict (title, tagline, price, etc.)
        guide_text:  the full guide content (plain text)
        prompts:     list of dicts: {label, use_case, prompt}
        output_path: where to write the .pdf

    Returns:
        Path to generated PDF
    """
    styles = make_styles()

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.85*inch,
        rightMargin=0.85*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title=product["title"],
        author="AIBusiness",
        subject=product.get("tagline", ""),
    )

    story = []

    # ── COVER ─────────────────────────────────────────────────────────────────
    story += cover_page(product, styles)

    # ── THE PROBLEM ───────────────────────────────────────────────────────────
    story += section_header("The Problem", "What's going wrong — and why it matters", styles)

    problem_text = parse_section(guide_text, ["THE PROBLEM", "PROBLEM THIS SOLVES", "WHAT'S WRONG"])
    if not problem_text:
        problem_text = product.get("description", "")

    story.append(Paragraph(problem_text, styles["body"]))

    if product.get("who_its_for"):
        who = product["who_its_for"]
        story.append(Paragraph(
            f"<b>Who this is for:</b> {who}",
            ParagraphStyle("who", fontName="Helvetica", fontSize=10, leading=15,
                           textColor=colors.HexColor("#374151"),
                           backColor=LIGHT_AMBER, borderPad=8, spaceAfter=8)
        ))

    story.append(Spacer(1, 0.15*inch))

    # ── WHAT YOU'LL HAVE AFTER ────────────────────────────────────────────────
    story += section_header("Outcomes", "What you'll have after this", styles)

    features = product.get("features", [])
    if not features:
        features = parse_bullets(guide_text, "WHAT YOU'LL HAVE") or parse_bullets(guide_text, "OUTCOMES")

    if features:
        story.append(outcome_table(features, styles))

    story.append(Spacer(1, 0.15*inch))

    # ── STEP BY STEP ──────────────────────────────────────────────────────────
    story += section_header("The Fix", "Step-by-step implementation", styles)

    steps = parse_steps(guide_text)
    if steps:
        for step in steps:
            body_text = " ".join(step["body"])
            block = KeepTogether([
                Paragraph(
                    f"<b>Step {step['num']} — {step['title']}</b>",
                    styles["h3"]
                ),
                Paragraph(body_text, styles["step_body"]) if body_text else Spacer(1, 4),
            ])
            story.append(block)
    else:
        # Fallback: render guide as flowing paragraphs
        for para in guide_text.split("\n\n"):
            stripped = para.strip()
            if stripped and not stripped.startswith("==="):
                story.append(Paragraph(stripped, styles["body"]))

    story.append(Spacer(1, 0.2*inch))

    # ── TEMPLATES / TOOL RECOMMENDATIONS ─────────────────────────────────────
    tools_section = parse_section(guide_text, ["TOOLS NEEDED", "TOOLS", "RECOMMENDED TOOLS", "FREE TOOLS"])
    if tools_section:
        story.append(hr())
        story += section_header("Tools", "Recommended tools (all free to start)", styles)

        tool_lines = [l.strip() for l in tools_section.split(".") if l.strip()]
        for tl in tool_lines[:5]:
            story.append(Paragraph(f"&#10003;  {tl}", styles["bullet"]))

        story.append(Spacer(1, 0.1*inch))

    # ── QUICK WIN ─────────────────────────────────────────────────────────────
    quick_win = parse_section(guide_text, ["QUICK WIN", "FIRST STEP", "START HERE"])
    if quick_win:
        story.append(hr())
        qw_data = [[Paragraph(
            f"<b>Quick Win:</b> {quick_win}",
            ParagraphStyle("qw", fontName="Helvetica", fontSize=10.5, leading=16,
                           textColor=colors.HexColor("#065f46"))
        )]]
        qw_table = Table(qw_data, colWidths=[6.8*inch])
        qw_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), LIGHT_GREEN),
            ("TOPPADDING", (0,0), (-1,-1), 12),
            ("BOTTOMPADDING", (0,0), (-1,-1), 12),
            ("LEFTPADDING", (0,0), (-1,-1), 14),
            ("RIGHTPADDING", (0,0), (-1,-1), 14),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), [6,6,6,6]),
            ("BOX", (0,0), (-1,-1), 0.5, GREEN),
        ]))
        story.append(qw_table)
        story.append(Spacer(1, 0.15*inch))

    # ── AI PROMPT LIBRARY ─────────────────────────────────────────────────────
    story.append(PageBreak())
    story += section_header(
        "AI Prompt Library",
        "Do it yourself — with AI guidance",
        styles,
    )

    story.append(Paragraph(
        "These prompts are tested and ready to copy-paste into ChatGPT or Claude. "
        "Each one handles a specific part of the implementation so you can use AI "
        "as your assistant throughout the process. Replace anything in [brackets] with your details.",
        styles["body"]
    ))

    # How-to-use banner
    how_data = [[Paragraph(
        "<b>How to use these prompts:</b> Copy the prompt text below, paste it into ChatGPT or Claude, "
        "fill in the [bracketed] details specific to your business, and hit send. "
        "The AI will guide you through that step.",
        ParagraphStyle("how", fontName="Helvetica", fontSize=9.5, leading=14,
                       textColor=colors.HexColor("#1e1b4b"))
    )]]
    how_table = Table(how_data, colWidths=[6.8*inch])
    how_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_PURPLE),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("BOX", (0,0), (-1,-1), 0.5, PURPLE),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [6,6,6,6]),
    ]))
    story.append(how_table)
    story.append(Spacer(1, 0.15*inch))

    if prompts:
        for p in prompts:
            story.append(prompt_box(
                p.get("label", ""),
                p.get("use_case", ""),
                p.get("prompt", ""),
                styles,
            ))
    else:
        story.append(Paragraph("(Prompts being generated)", styles["body_muted"]))

    # ── GUARANTEE ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*inch))
    story.append(hr(GREEN))

    guar_data = [[Paragraph(
        "<b>30-Day Money-Back Guarantee</b>  —  Follow the steps and it doesn't work for you? "
        "Email us within 30 days for a full refund. No questions. These are built from real problems — "
        "if it doesn't fix yours, you don't pay.",
        ParagraphStyle("guar2", fontName="Helvetica", fontSize=9.5, leading=15,
                       textColor=colors.HexColor("#065f46"))
    )]]
    guar_table = Table(guar_data, colWidths=[6.8*inch])
    guar_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_GREEN),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
    ]))
    story.append(guar_table)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3*inch))
    story.append(hr())
    story.append(Paragraph(
        f"AIBusiness · Generated {datetime.now().strftime('%B %d, %Y')} · "
        "This is a living document — AI updates it when tools or best practices change. "
        "Check back for the latest version.",
        styles["footer"]
    ))

    doc.build(story)
    return output_path


# ── CLI test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    # Quick smoke test with dummy data
    ROOT = Path(__file__).parent.parent
    test_product = {
        "title": "Stop Chasing Payments: Automated Invoice Follow-Up",
        "tagline": "Set it up once. Get paid automatically.",
        "description": "Tired of chasing clients for money you already earned? This blueprint sets up a 3-step automated payment reminder sequence that runs without you.",
        "features": [
            "Works with Wave, Stripe, FreshBooks, or Gmail",
            "Day 3, 7, and 14 reminders fully automated",
            "Copy-paste email templates included",
            "Free tools for all three setup options",
            "Setup time under 45 minutes",
        ],
        "who_its_for": "Freelancers, consultants, and small agencies who invoice clients",
        "price_usd": 29,
        "product_type": "blueprint",
    }
    test_guide = """THE PROBLEM THIS SOLVES
You deliver the work, send the invoice, then spend weeks chasing payment. This blueprint eliminates that.

WHAT YOU'LL HAVE AFTER
- Automated day-3, 7, and 14 follow-up emails running without you
- Professional email templates that get clients to pay

TOOLS NEEDED
Wave (free), Stripe, Zapier.

Step 1: Move your invoicing to a tool with automation.
Recommended: Wave (free) or Stripe.

Step 2: Enable automatic payment reminders.
Go to Settings > Reminders. Turn on 3-day, 7-day, 14-day.

Step 3: Customize your reminder templates.
Day 3: friendly nudge. Day 7: clear ask. Day 14: firm notice.

Step 4: Add a late fee clause to your invoices.
Even 1.5% per month motivates faster payment.

QUICK WIN
Enable the 3-day automatic reminder in Wave or Stripe today — it takes 5 minutes and will catch most late payers before they become a problem.
"""
    test_prompts = [
        {
            "label": "Write a day-3 payment reminder",
            "use_case": "When you need a polite follow-up email for an overdue invoice",
            "prompt": "Write a short, friendly payment reminder email for a [freelancer/consultant] to send to [client name]. The invoice is for [project name], amount $[amount], and is 3 days overdue. Keep it warm, not pushy. Include a direct payment link placeholder [PAYMENT_LINK]. Under 100 words."
        },
        {
            "label": "Draft a late fee policy",
            "use_case": "When you want to add a late fee clause to your invoices",
            "prompt": "Write a professional late fee clause for a freelance invoice. I charge [1.5%] per month on overdue balances. Payment is due within [30] days. Make it firm but not aggressive — one paragraph, plain English, suitable for adding to the footer of a client invoice."
        },
    ]

    out = ROOT / "products" / "test-pdf-output.pdf"
    out.parent.mkdir(exist_ok=True)
    result = build_pdf(test_product, test_guide, test_prompts, out)
    print(f"✅ Test PDF written to: {result}")
    print(f"   Size: {result.stat().st_size / 1024:.1f} KB")
