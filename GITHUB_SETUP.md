# GitHub Pages + Gumroad Setup Guide

Follow these steps once to get the site live. After that, the AI cycle handles updates automatically.

---

## Step 1 — Create a GitHub repo

1. Go to **github.com/new**
2. Name it: `worksmarter-tools` (or anything you like)
3. Set it to **Public** (required for free GitHub Pages)
4. **Do not** add a README or .gitignore (we already have those)
5. Click **Create repository**

---

## Step 2 — Push this folder to GitHub

Open Terminal, paste these commands one at a time.
Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

```bash
cd ~/Desktop/makethatmoney

git init
git add index.html products/ state/offers.json scripts/generate_site.py scripts/deploy_site.sh AGENTS.md README.md .gitignore

git commit -m "first commit: launch WorkSmarter.tools"

git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/worksmarter-tools.git
git push -u origin main
```

---

## Step 3 — Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under "Source", select **Deploy from a branch**
4. Branch: **main** / folder: **/ (root)**
5. Click **Save**

Your site will be live at:
`https://YOUR_GITHUB_USERNAME.github.io/worksmarter-tools/`

(Takes about 60 seconds for the first deploy.)

---

## Step 4 — List products on Gumroad

For each product, do this on gumroad.com:

1. Go to **app.gumroad.com** → New Product
2. Copy the title and description from the product's `gumroad_listing.json` file
3. Set the price from `gumroad_listing.json`
4. Upload the `content.txt` file from the same product folder
5. Publish — Gumroad gives you a URL like `https://yourname.gumroad.com/l/xyz`

Products to list:

| Product | Price | File |
|---------|-------|------|
| Stop Chasing Payments | $29 | products/chasing_payments/ |
| Monthly Finance Tracker | $19 | products/finance_planning_spreadsheet/ |
| Instagram Ads Conversion Fix | $19 | products/instagram_ads_no_clients/ |
| 48-Hour AI Automation Audit | $49 | (service — use a Gumroad "call" or custom checkout) |

---

## Step 5 — Add Gumroad URLs to product files

Once you have the Gumroad links, paste them into the `listing_url` field in each product's `gumroad_listing.json`. Example:

```json
{
  "listing_url": "https://yourname.gumroad.com/l/stop-chasing-payments",
  "status": "live"
}
```

Then run:
```bash
cd ~/Desktop/makethatmoney
python3 scripts/generate_site.py
./scripts/deploy_site.sh "add Gumroad buy links"
```

The buttons on your live site will now go to Gumroad checkout.

---

## How auto-updates work after setup

Once git is set up, replace your current loop command with:

```bash
cd ~/Desktop/makethatmoney
export OPENCODE_ENABLE_EXA=1
./scripts/deploy_after_cycle.sh 45
```

Every 45 minutes, the AI runs a research cycle. If it creates or updates any products, it automatically:
1. Regenerates `index.html`
2. Commits the changes
3. Pushes to GitHub
4. GitHub Pages re-deploys (~30 seconds)

New products appear on your live site without you touching anything.

---

## Updating a product manually

To change a price, description, or add a Gumroad URL:

1. Edit the product's `gumroad_listing.json` directly
2. Run `./scripts/deploy_site.sh "your change note"`

That's it.
