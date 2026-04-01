#!/usr/bin/env python3
"""
generate_gumroad_page.py
Creates a Gumroad-embedded checkout page for each product.
"""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent
PRODUCTS_DIR = ROOT / "products"
GUMROAD_PAGES_DIR = ROOT / "gumroad_pages"
GUMROAD_PAGES_DIR.mkdir(exist_ok=True)

CONFIG = json.loads((ROOT / "config.json").read_text())
BIZ = CONFIG["business"]

def load_products():
    products = []
    if not PRODUCTS_DIR.exists():
        return products
    
    for folder in sorted(PRODUCTS_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        listing_file = folder / "listing.json"
        if listing_file.exists():
            try:
                data = json.loads(listing_file.read_text())
                if data.get("status") != "retired":
                    products.append(data)
            except:
                pass
    return products

def generate_gumroad_page(product):
    """Generate a standalone page with embedded Gumroad checkout."""
    
    title = product.get("title", "Product")
    price = product.get("price_usd", 29)
    description = product.get("description", "")
    features = product.get("features", [])
    who = product.get("who_its_for", "")
    slug = product.get("slug", "")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {BIZ['name']}</title>
    <script src="https://gumroad.com/js/gumroad.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 700px; margin: 0 auto; }}
        .card {{ 
            background: white;
            border-radius: 16px;
            padding: 48px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ font-size: 2.5rem; margin-bottom: 8px; color: #1a1a2e; }}
        .tagline {{ font-size: 1.25rem; color: #666; margin-bottom: 32px; }}
        .price {{ 
            font-size: 3rem; 
            font-weight: 800; 
            color: #667eea;
            margin: 24px 0;
        }}
        .description {{ 
            font-size: 1.1rem; 
            color: #555;
            margin: 24px 0;
            line-height: 1.8;
        }}
        .features {{ margin: 32px 0; }}
        .features h3 {{ margin-bottom: 16px; color: #1a1a2e; }}
        .features ul {{ list-style: none; }}
        .features li {{ 
            padding: 12px 0;
            padding-left: 32px;
            position: relative;
        }}
        .features li::before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #22c55e;
            font-weight: bold;
        }}
        .who {{ 
            background: #f3f4f6;
            padding: 20px;
            border-radius: 8px;
            margin: 24px 0;
        }}
        .who h3 {{ margin-bottom: 8px; color: #1a1a2e; }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 48px;
            border-radius: 12px;
            font-size: 1.25rem;
            font-weight: 600;
            text-decoration: none;
            margin: 32px 0;
            transition: transform 0.2s, box-shadow 0.2s;
            border: none;
            cursor: pointer;
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        .guarantee {{
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            margin-top: 24px;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: white;
            text-decoration: none;
            opacity: 0.8;
        }}
        .back-link:hover {{ opacity: 1; }}
        @media (max-width: 600px) {{
            .card {{ padding: 32px 24px; }}
            h1 {{ font-size: 1.75rem; }}
            .price {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← Back to all products</a>
        <div class="card">
            <h1>{title}</h1>
            <p class="tagline">{product.get('tagline', '')}</p>
            
            <div class="price">${price}</div>
            
            <div class="description">{description}</div>
            
            <div class="features">
                <h3>What's included:</h3>
                <ul>
"""
    
    for feature in features:
        html += f"                    <li>{feature}</li>\n"
    
    html += f"""                </ul>
            </div>
            
            <div class="who">
                <h3>Who this is for</h3>
                <p>{who}</p>
            </div>
            
            <a href="https://gum.co/{slug}" class="cta-button gumroad-button" target="_blank">
                Get Instant Access →
            </a>
            
            <p class="guarantee">
                🔒 Secure checkout • 30-day money-back guarantee • Instant download
            </p>
        </div>
    </div>
    
    <script>
        // Track which product page this is
        localStorage.setItem('lastViewedProduct', '{slug}');
    </script>
</body>
</html>"""
    
    output_file = GUMROAD_PAGES_DIR / f"{slug}.html"
    output_file.write_text(html)
    return output_file

def main():
    print("\n📄 Generating Gumroad checkout pages...")
    
    products = load_products()
    if not products:
        print("   No products found")
        return
    
    generated = 0
    for product in products:
        if product.get("status") == "live":
            output_file = generate_gumroad_page(product)
            print(f"   ✅ {product['title']} → {output_file.name}")
            generated += 1
    
    print(f"\n✅ Generated {generated} checkout page(s)")
    print(f"   Location: {GUMROAD_PAGES_DIR}/")

if __name__ == "__main__":
    main()
