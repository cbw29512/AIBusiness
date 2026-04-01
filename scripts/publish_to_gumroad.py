#!/usr/bin/env python3
"""
publish_to_gumroad.py
Automatically publishes new products to Gumroad via API, uploads the PDF,
and saves the listing URL back to listing.json so the site buy buttons work.

Run directly:   python3 scripts/publish_to_gumroad.py
Or called by:   engine/loop.py after each build cycle
"""

import io
import json
import sys
import uuid
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))

CONFIG = json.loads((ROOT / "config.json").read_text())
TOKEN  = CONFIG.get("gumroad", {}).get("access_token", "")
USERNAME = CONFIG.get("business", {}).get("gumroad_username", "")

GUMROAD_API = "https://api.gumroad.com/v2"


# ── helpers ──────────────────────────────────────────────────────────────────

def _api_post(endpoint: str, fields: dict) -> dict:
    """POST form-encoded data to the Gumroad API."""
    fields["access_token"] = TOKEN
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        f"{GUMROAD_API}/{endpoint}",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _multipart_post(url: str, fields: dict, file_field: str, file_path: Path) -> dict:
    """POST multipart/form-data — used for file uploads."""
    boundary = uuid.uuid4().hex
    crlf = b"\r\n"

    body = io.BytesIO()
    for name, value in fields.items():
        body.write(f"--{boundary}{crlf.decode()}".encode())
        body.write(f'Content-Disposition: form-data; name="{name}"{crlf.decode()}{crlf.decode()}'.encode())
        body.write(value.encode())
        body.write(crlf)

    # File part
    filename = file_path.name
    body.write(f"--{boundary}{crlf.decode()}".encode())
    body.write(f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"{crlf.decode()}'.encode())
    body.write(f"Content-Type: application/pdf{crlf.decode()}{crlf.decode()}".encode())
    body.write(file_path.read_bytes())
    body.write(crlf)
    body.write(f"--{boundary}--{crlf.decode()}".encode())

    raw = body.getvalue()
    req = urllib.request.Request(
        url,
        data=raw,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


# ── core logic ────────────────────────────────────────────────────────────────

def create_gumroad_product(listing: dict) -> dict:
    """Create the product listing on Gumroad. Returns the API response."""
    desc_parts = [listing.get("description", "")]

    who = listing.get("who_its_for", "")
    if who:
        desc_parts.append(f"\n\nWho it's for:\n{who}")

    features = listing.get("features", [])
    if features:
        desc_parts.append("\n\nWhat you get:")
        for f in features:
            desc_parts.append(f"• {f}")

    prompt_count = listing.get("prompt_count", 0)
    if prompt_count:
        desc_parts.append(f"\n✅ Includes {prompt_count} tested AI prompts — copy, paste, done.")

    desc_parts.append("\n\n30-day money-back guarantee. No questions asked.")

    description = "\n".join(desc_parts)
    price_cents  = int(listing.get("price_usd", 19) * 100)
    category     = listing.get("category", "business")
    tags         = ",".join(["small business", "productivity", "templates", category])

    return _api_post("products", {
        "name":       listing["title"],
        "price":      str(price_cents),
        "description": description,
        "permalink":  listing["slug"],
        "tags":       tags,
    })


def upload_pdf(gumroad_id: str, pdf_path: Path) -> bool:
    """Upload the PDF to an existing Gumroad product."""
    url = f"{GUMROAD_API}/products/{gumroad_id}/product_files"
    try:
        result = _multipart_post(url, {"access_token": TOKEN}, "file", pdf_path)
        return result.get("success", False)
    except Exception as e:
        print(f"       ⚠️  Upload error: {e}")
        return False


def publish_product(product_dir: Path) -> bool:
    """
    Publish one product to Gumroad if not already live.
    Updates listing.json with the Gumroad URL so buy buttons work.
    Returns True if newly published.
    """
    listing_file = product_dir / "listing.json"
    if not listing_file.exists():
        return False

    listing = json.loads(listing_file.read_text())

    # Skip if already live
    if listing.get("status") == "live" and listing.get("listing_url"):
        print(f"   ⏭️  Already live: {listing['title']}")
        return False

    print(f"\n   📤 Publishing: {listing['title']}")

    try:
        result = create_gumroad_product(listing)
    except Exception as e:
        print(f"   ❌ API error: {e}")
        return False

    if not result.get("success"):
        msg = result.get("message", "Unknown error")
        # Permalink already taken = product exists under a different ID
        if "permalink" in msg.lower():
            print(f"   ⚠️  Permalink taken — try editing slug in listing.json")
        else:
            print(f"   ❌ Gumroad error: {msg}")
        return False

    product_data = result["product"]
    gumroad_id   = product_data["id"]
    permalink    = product_data.get("permalink", listing["slug"])
    listing_url  = f"https://{USERNAME}.gumroad.com/l/{permalink}"

    print(f"   ✅ Product created → {listing_url}")

    # Upload PDF
    pdf_name = listing.get("pdf_file", f"{listing['slug']}.pdf")
    pdf_path = product_dir / pdf_name
    if pdf_path.exists():
        ok = upload_pdf(gumroad_id, pdf_path)
        if ok:
            print(f"   📄 PDF uploaded: {pdf_path.name}")
        else:
            print(f"   ⚠️  PDF upload failed — buyer won't get the file until you upload manually")
    else:
        print(f"   ⚠️  PDF not found at {pdf_path}")

    # Save back to listing.json
    listing["listing_url"] = listing_url
    listing["gumroad_id"]  = gumroad_id
    listing["status"]      = "live"
    listing["updated_at"]  = datetime.now().isoformat()
    listing_file.write_text(json.dumps(listing, indent=2))

    return True


def run() -> int:
    """
    Publish all pending products. Returns count of newly published products.
    Called by loop.py after each build cycle.
    """
    if not TOKEN:
        print("   ⚠️  No Gumroad token in config.json — skipping Gumroad publish")
        return 0
    if not USERNAME:
        print("   ⚠️  No Gumroad username in config.json — skipping Gumroad publish")
        return 0

    products_dir = ROOT / "products"
    if not products_dir.exists():
        return 0

    published = 0
    for product_dir in sorted(products_dir.iterdir()):
        if product_dir.is_dir() and (product_dir / "listing.json").exists():
            if publish_product(product_dir):
                published += 1

    return published


def main():
    print("\n🚀 Gumroad Publisher")
    print(f"   Account: {USERNAME}.gumroad.com")
    print(f"   Token:   {'✅ found' if TOKEN else '❌ missing'}")

    count = run()

    if count:
        print(f"\n✅ Published {count} new product(s)")
        # Regenerate site so buy buttons point to real URLs
        import subprocess
        subprocess.run(
            [sys.executable, str(ROOT / "site" / "generate.py")],
            cwd=ROOT, capture_output=True
        )
        print("   Site regenerated with live Gumroad links")
    else:
        print("\n   Nothing new to publish")


if __name__ == "__main__":
    main()
