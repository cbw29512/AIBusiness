#!/usr/bin/env python3
"""
researcher.py
Fetches current, real setup instructions from tool websites before the guide is written.
This ensures every step in the guide is accurate and up to date — not guessed.

What it does per tool:
  1. Searches DuckDuckGo for the tool's help/setup page
  2. Fetches the most relevant result
  3. Extracts the useful text (strips nav, ads, footers)
  4. Returns a plain-text summary to include in the Ollama prompt

The guide writer then uses this real content instead of making things up.
"""

import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from html.parser import HTMLParser

# Import the verified knowledge base as a fallback
try:
    sys.path.insert(0, str(Path(__file__).parent))
    import knowledge_base as kb
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False

# ── Known help page URLs for common tools ─────────────────────────────────────
# Used first so we skip search and go straight to the right page.
KNOWN_HELP_URLS = {
    "wave": [
        "https://support.waveapps.com/hc/en-us/articles/208621816-Automatic-payment-reminders",
        "https://support.waveapps.com/hc/en-us/articles/208621696-Create-and-send-an-invoice",
    ],
    "stripe": [
        "https://stripe.com/docs/billing/invoices/reminder-emails",
        "https://stripe.com/docs/invoicing/overview",
    ],
    "zapier": [
        "https://zapier.com/help/create/basics/create-zaps",
        "https://zapier.com/blog/beginners-guide-zapier/",
    ],
    "make": [
        "https://www.make.com/en/help/scenarios/creating-a-scenario",
    ],
    "gmail": [
        "https://support.google.com/mail/answer/6594?hl=en",
    ],
    "calendly": [
        "https://help.calendly.com/hc/en-us/articles/223195488-Getting-started-with-Calendly",
    ],
    "acuity": [
        "https://help.acuityscheduling.com/hc/en-us/articles/219149648-Getting-started-with-Acuity-Scheduling",
    ],
    "mailchimp": [
        "https://mailchimp.com/help/getting-started-with-email/",
        "https://mailchimp.com/help/create-an-email-campaign/",
    ],
    "convertkit": [
        "https://help.kit.com/en/articles/2502558-getting-started-with-convertkit",
    ],
    "google sheets": [
        "https://support.google.com/docs/answer/6000292?hl=en",
    ],
    "notion": [
        "https://www.notion.so/help/guides/getting-started-with-notion",
    ],
    "typeform": [
        "https://www.typeform.com/help/a/getting-started-with-typeform-360029249271/",
    ],
    "chatgpt": [
        "https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api",
    ],
    "claude": [
        "https://docs.anthropic.com/en/docs/intro-to-claude",
    ],
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# ── HTML text extractor ────────────────────────────────────────────────────────
class TextExtractor(HTMLParser):
    """Strip HTML tags and extract readable text."""

    SKIP_TAGS = {"script", "style", "nav", "header", "footer", "aside",
                 "noscript", "iframe", "form", "button", "input"}

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._skip = 0
        self._current_tag = ""

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        if tag in self.SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self._skip = max(0, self._skip - 1)

    def handle_data(self, data):
        if self._skip == 0:
            cleaned = data.strip()
            if cleaned and len(cleaned) > 2:
                self.text_parts.append(cleaned)

    def get_text(self):
        return " ".join(self.text_parts)


def clean_html(html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    text = parser.get_text()
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove very short fragments and noise
    lines = [l.strip() for l in text.split('.') if len(l.strip()) > 20]
    return '. '.join(lines[:120])  # cap at ~120 sentences


def fetch_url(url: str, timeout: int = 12) -> str:
    """Fetch a URL and return cleaned text content."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = "utf-8"
            content_type = resp.headers.get("Content-Type", "")
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].strip()
            html = resp.read().decode(charset, errors="replace")
            return clean_html(html)
    except Exception as e:
        return f"[Could not fetch {url}: {e}]"


def search_duckduckgo(query: str) -> list[str]:
    """Search DuckDuckGo and return top result URLs."""
    encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Extract result links
        urls = re.findall(r'href="(https?://[^"&]+)"', html)
        # Filter out DuckDuckGo's own redirect links and ads
        clean = []
        for u in urls:
            if "duckduckgo.com" not in u and "ad_provider" not in u:
                clean.append(u)
            if len(clean) >= 3:
                break
        return clean
    except Exception:
        return []


def research_tool(tool_name: str) -> dict:
    """
    Research a specific tool and return current setup instructions.
    Returns: {tool, url, content, success}
    """
    tool_key = tool_name.lower().strip()
    print(f"     🔍 Researching: {tool_name}...")

    # Try known help URLs first
    known = KNOWN_HELP_URLS.get(tool_key, [])
    urls_to_try = known.copy()

    # If not in known list, search for it
    if not urls_to_try:
        query = f"{tool_name} how to set up step by step guide 2025 site:help.{tool_key}.com OR site:support.{tool_key}.com OR site:{tool_key}.com/help"
        search_results = search_duckduckgo(query)
        if not search_results:
            # Fallback: general search
            search_results = search_duckduckgo(f"{tool_name} setup tutorial for beginners 2025")
        urls_to_try = search_results[:2]

    for url in urls_to_try[:2]:
        content = fetch_url(url)
        if content and not content.startswith("[Could not fetch"):
            # Extract the most useful portion
            useful = content[:3000]
            print(f"       ✅ Got {len(useful)} chars from {url}")
            return {"tool": tool_name, "url": url, "content": useful, "success": True}
        time.sleep(0.5)

    # Live fetch failed — fall back to verified knowledge base
    if KB_AVAILABLE:
        kb_content = kb.get_tool_docs(tool_name)
        if kb_content:
            print(f"       📚 Using verified knowledge base for {tool_name}")
            # kb_content already contains a header — return raw content so the
            # outer wrapper in research_for_problem doesn't double-up headers.
            # We return it without the outer "CURRENT SETUP INSTRUCTIONS" wrapper.
            return {"tool": tool_name, "url": "__kb__", "content": kb_content, "success": True}

    print(f"       ⚠️  Could not fetch docs for {tool_name}")
    return {"tool": tool_name, "url": "", "content": "", "success": False}


# Tool name patterns per problem category
CATEGORY_TOOLS = {
    "payment_collection": ["Wave", "Stripe", "Zapier"],
    "customer_followup": ["Mailchimp", "Zapier", "Gmail"],
    "online_booking": ["Calendly", "Acuity"],
    "social_proof": ["Google Business Profile", "Zapier"],
    "lead_capture": ["Mailchimp", "Typeform", "Zapier"],
    "onboarding": ["Notion", "Typeform", "Gmail"],
    "pricing": ["Wave", "Stripe"],
    "proposals": ["Notion", "Google Docs"],
    "email_marketing": ["Mailchimp", "ConvertKit"],
    "no_show_prevention": ["Calendly", "Gmail", "Zapier"],
    "cash_flow": ["Wave", "Google Sheets"],
    "refunds_complaints": ["Stripe", "Gmail"],
    "ai_content_creation": ["ChatGPT", "Claude"],
    "ai_repurposing": ["ChatGPT", "Claude"],
    "ai_audience_growth": ["ChatGPT", "Claude"],
    "ai_email_list": ["Mailchimp", "ConvertKit", "ChatGPT"],
    "ai_client_content": ["ChatGPT", "Claude", "Notion"],
    "ai_short_form": ["ChatGPT", "Claude"],
}


def research_for_problem(problem: dict) -> str:
    """
    Research all relevant tools for a problem category.
    Returns a formatted string ready to paste into the Ollama prompt.
    """
    category = problem.get("category", "")
    tools = CATEGORY_TOOLS.get(category, [])

    # Also extract any tools mentioned directly in the problem
    problem_text = problem.get("problem_statement", "") + " " + problem.get("why_fixable", "")
    for tool in ["Wave", "Stripe", "Zapier", "Calendly", "Mailchimp", "Gmail",
                 "Make", "Notion", "Typeform", "ConvertKit", "ChatGPT", "Claude", "Acuity"]:
        if tool.lower() in problem_text.lower() and tool not in tools:
            tools.append(tool)

    if not tools:
        return ""

    print(f"   🌐  Researching {len(tools)} tool(s): {', '.join(tools)}")
    results = []

    for tool in tools[:3]:  # Cap at 3 tools to keep prompts manageable
        data = research_tool(tool)
        if data["success"]:
            if data["url"] == "__kb__":
                # Knowledge base result — already has its own header
                results.append(data["content"][:2000])
            else:
                # Live fetch result — wrap with standard header
                results.append(
                    f"=== CURRENT SETUP INSTRUCTIONS FOR {data['tool'].upper()} ===\n"
                    f"Source: {data['url']}\n\n"
                    f"{data['content'][:1500]}\n"
                )
        time.sleep(0.3)

    if not results:
        # All live fetches failed — try knowledge base for entire category
        if KB_AVAILABLE:
            kb_content = kb.get_docs_for_category(category)
            if kb_content:
                print(f"   📚 Using knowledge base fallback for category: {category}")
                return (
                    "\n\nHERE IS VERIFIED DOCUMENTATION FOR THESE TOOLS (sourced April 2026):\n"
                    "(Use this information to write accurate setup steps. "
                    "Menu paths and button names are current as of the verification date.)\n\n"
                    + kb_content
                )
        return ""

    return (
        "\n\nHERE IS CURRENT, LIVE DOCUMENTATION FETCHED FROM THE TOOL WEBSITES:\n"
        "(Use this information to write accurate, current setup steps. "
        "If the documentation shows a specific menu path or button name, use it exactly.)\n\n"
        + "\n\n".join(results)
    )


if __name__ == "__main__":
    # Test with a sample problem
    problem = {
        "category": "payment_collection",
        "problem_statement": "Freelancers spend hours chasing late invoice payments",
        "why_fixable": "Wave and Stripe both have built-in automated reminder features",
    }
    result = research_for_problem(problem)
    print(f"\nResearch result ({len(result)} chars):")
    print(result[:1000])
