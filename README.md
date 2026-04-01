# AIBusiness

AI finds real business problems. Builds the fix. Sells it online. Runs on your local AI (Ollama).

## How it works

```
Scout → finds fixable business problems (including AI/creator tools)
Builder → local Ollama AI writes the complete guide/template
Site → index.html auto-updates with new products
Deploy → pushes to GitHub Pages automatically
```

## Quick start

### Step 1 — Start Ollama
Open Terminal and run:
```bash
ollama serve
```
Keep this tab open. In a new tab:
```bash
ollama pull llama3.2
```

### Step 2 — Check setup
```bash
cd ~/Desktop/AIBusiness
./scripts/check.sh
```

### Step 3 — Run the engine (one cycle to test)
```bash
./scripts/start.sh
```

### Step 4 — Run continuously
```bash
./scripts/start.sh loop 60
```
Runs every 60 minutes. Each cycle: scouts 3 problems, builds 1 product, updates the site.

---

## GitHub Pages (to go live)

```bash
cd ~/Desktop/AIBusiness
git init
git add index.html products/ site/ engine/ scripts/ config.json README.md .gitignore
git commit -m "launch: AIBusiness"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aibusiness.git
git push -u origin main
```

Then on GitHub: Settings → Pages → Branch: main / root → Save.

Add your repo URL to config.json → deploy → github_repo.

---

## Gumroad setup

1. Go to app.gumroad.com and create a free account
2. Add your username to config.json → business → gumroad_username
3. For each product in products/:
   - Open the folder
   - Use README.md as a guide for listing it on Gumroad
   - Paste the Gumroad URL into listing.json → listing_url
   - Change status to "live" in listing.json
4. Run: `python3 site/generate.py` to update buy buttons

---

## File structure

```
AIBusiness/
├── engine/
│   ├── ollama_client.py   ← all AI calls go through here
│   ├── scout.py           ← finds business problems
│   ├── builder.py         ← builds the digital fix
│   └── loop.py            ← orchestrates everything
├── products/              ← generated products (auto-created)
│   └── <slug>/
│       ├── listing.json   ← title, price, gumroad url
│       ├── guide.txt      ← the deliverable buyers receive
│       └── README.md
├── site/
│   └── generate.py        ← builds index.html from products/
├── scripts/
│   ├── start.sh           ← run the engine
│   └── check.sh           ← diagnose setup
├── state/
│   └── problems.json      ← problem queue
├── config.json            ← all settings
├── index.html             ← the live site (auto-generated)
└── README.md
```

---

## Customizing what the AI looks for

Edit config.json → scout → problems_per_cycle to control how many problems are found per cycle.

The AI already searches across these categories:
- Payment collection / invoice follow-up
- Customer follow-up automation
- Online booking
- Review generation
- Lead capture
- Client onboarding
- Pricing confidence
- Proposals
- Email marketing
- No-show prevention
- Cash flow tracking
- **AI content creation for creators** ← creator niche
- **AI content repurposing** ← creator niche
- **AI audience growth research** ← creator niche
- **AI email list building** ← creator niche
- **AI client content at scale** ← creator niche
- **AI short-form content** ← creator niche

Add new categories in engine/scout.py → PROBLEM_SEEDS.
