#!/usr/bin/env python3
"""
publish_to_gumroad.py
Automatically publishes products to Gumroad via API.
"""

import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "engine"))

CONFIG = json.loads((ROOT / "config.json").read_text())
TOKEN = CONFIG["gumroad"]["access_token"]
USERNAME = CONFIG["business"]["gumroad_username"]

def publish_product(product_dir: Path) -> dict:
    """Publish a product to Gumroad."""
    listing_file = product_dir / "listing.json"
    if not listing_file.exists():
        return {"error": "No listing.json found"}
    
    listing = json.loads(listing_file.read_text())
    
    # Skip if already published
    if listing.get("status") == "live" and listing.get("listing_url"):
        print(f"   Already published: {listing['title']}")
        return listing
    
    # Build description
    description = f"""{listing['description']}

Who it's for:
{listing['who_its_for']}

Features:
"""
    for feature in listing.get("features", []):
        description += f"• {feature}\n"
    
    description += f"""
What you get: A complete PDF guide with step-by-step instructions and ready-to-use templates.

Price: ${listing['price_usd']}
"""
    
    # Create product on Gumroad using POST with form data
    url = "https://api.gumroad.com/v2/products"
    
    data = urllib.parse.urlencode({
        "access_token": TOKEN,
        "name": listing["title"],
        "price": listing["price_usd"] * 100,  # Gumroad uses cents
        "description": description,
        "permalink": listing["slug"],
        "tags": ",".join(["freelancer", "business", "templates", listing["category"]]),
    }).encode()
    
    try:
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("success"):
            product_data = result.get("product", {})
            listing_url = f"https://{USERNAME}.gumroad.com/l/{product_data.get('permalink', listing['slug'])}"
            
            # Update listing
            listing["listing_url"] = listing_url
            listing["status"] = "live"
            listing["gumroad_id"] = product_data.get("id")
            listing["updated_at"] = datetime.now().isoformat()
            listing_file.write_text(json.dumps(listing, indent=2))
            
            print(f"   ✅ Published: {listing['title']}")
            print(f"   📎 URL: {listing_url}")
            return listing
        else:
            print(f"   ❌ Failed: {result.get('message', 'Unknown error')}")
            return {"error": result.get("message")}
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"error": str(e)}

def upload_file_to_product(gumroad_id: str, pdf_path: Path):
    """Upload PDF file to existing Gumroad product."""
    url = f"https://api.gumroad.com/v2/products/{gumroad_id}/files"
    
    try:
        # Build multipart form
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        
        body = []
        body.append(f"--{boundary}")
        body.append(f'Content-Disposition: form-data; name="access_token"')
        body.append("")
        body.append(TOKEN)
        
        body.append(f"--{boundary}")
        body.append(f'Content-Disposition: form-data; name="file"; filename="{pdf_path.name}"')
        body.append("Content-Type: application/pdf")
        body.append("")
        body.append(pdf_path.read_bytes())
        
        body.append(f"--{boundary}--")
        
        data = "\r\n".join(body)
        
        req = urllib.request.Request(
            url,
            data=data.encode(),
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("success"):
            print(f"   ✅ File uploaded: {pdf_path.name}")
            return True
        else:
            print(f"   ⚠️ Upload issue: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"   ⚠️ Upload error: {e}")
        return False

def main():
    from datetime import datetime
    
    print("\n🚀 Publishing to Gumroad...")
    print(f"   Username: {USERNAME}")
    
    products_dir = ROOT / "products"
    if not products_dir.exists():
        print("   No products directory found")
        return
    
    published = 0
    for product_dir in products_dir.iterdir():
        if product_dir.is_dir():
            listing_file = product_dir / "listing.json"
            if listing_file.exists():
                listing = json.loads(listing_file.read_text())
                if listing.get("status") != "live":
                    result = publish_product(product_dir)
                    if result.get("status") == "live":
                        # Try to upload PDF
                        pdf_file = product_dir / listing.get("pdf_file", "")
                        if pdf_file.exists() and result.get("gumroad_id"):
                            upload_file_to_product(result["gumroad_id"], pdf_file)
                        published += 1
    
    print(f"\n✅ Published {published} product(s)")
    
    # Regenerate site
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "site" / "generate.py")], cwd=ROOT)
    print("   Site regenerated")

if __name__ == "__main__":
    main()
