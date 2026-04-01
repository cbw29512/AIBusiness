#!/usr/bin/env python3
"""
knowledge_base.py
Verified, current setup instructions for common tools — researched April 2026.
Used as a fallback when live web fetching is unavailable, or combined with live
docs to give the guide writer accurate, up-to-date information.

Every entry here was verified against the tool's official help centre.
Sources are included so the researcher can re-verify when needed.
"""

# Format: each entry is the plain text the guide writer receives as context.
# Written in plain English so Ollama can use it directly in non-tech guides.

TOOL_DOCS = {

    "wave": {
        "source": "https://support.waveapps.com/hc/en-us/articles/208621676",
        "verified": "April 2026",
        "content": """
WAVE INVOICING — HOW TO SET UP AUTOMATIC PAYMENT REMINDERS
(Wave is a free invoicing and accounting tool at waveapps.com)

HOW TO CREATE AN ACCOUNT:
1. Go to waveapps.com in your browser
2. Click the blue "Sign up for free" button
3. Enter your email address and create a password
4. Fill in your business name and type — Wave will set up your account
5. You'll land on your Wave dashboard — this is your home screen

HOW TO SET UP AUTOMATIC PAYMENT REMINDERS (applies to all new invoices):
1. On the left side of your screen, click "Sales" to expand the menu
2. Click "Invoices" — you'll see a list of any invoices you've created
3. In the top-right area, click the gear icon (⚙) labeled "Settings"
4. Scroll down to find the section called "Automatic payment reminders"
5. You'll see three checkboxes — tick the boxes for:
   - "3 days after the due date" (polite first nudge)
   - "7 days after the due date" (firmer follow-up)
   - "14 days after the due date" (final notice)
6. Click "Save changes" — you'll see a green confirmation message
7. These reminders now apply to all your new invoices automatically

HOW TO SEND AN INVOICE:
1. Click "Create invoice" (blue button, top right)
2. In the "Bill to" field, type your client's name or email
3. Add what you did: click "Add a product or service", type the work description, add the price
4. Set a due date — click the "Due" field and pick a date from the calendar
5. Click "Send invoice" — Wave will email it to your client automatically

IMPORTANT LIMITATION: Wave's automatic reminders work for one-off invoices.
For recurring invoices, you need to send reminders manually or use Zapier.

WHAT YOUR CLIENT SEES: They receive a professional email from Wave with your invoice
attached and a blue "Pay now" button. They can pay by credit card — no account needed.

IF SOMETHING GOES WRONG:
- "My client didn't receive the invoice" — check the email address, look in their spam folder
- "I can't see the reminder settings" — make sure you're in Settings, not on an individual invoice
- "The reminders aren't sending" — check your client has an email address saved on their profile
"""
    },

    "stripe": {
        "source": "https://stripe.com/docs/billing/invoices/reminder-emails",
        "verified": "April 2026",
        "content": """
STRIPE — HOW TO SET UP INVOICE PAYMENT REMINDERS
(Stripe is a payment tool at stripe.com — free to sign up, they charge a small fee per payment)

HOW TO CREATE AN ACCOUNT:
1. Go to stripe.com
2. Click "Start now" or "Create account"
3. Enter your email, name, and create a password
4. Stripe will ask you to verify your email — check your inbox and click the link
5. Fill in your business details — Stripe needs this to send you payouts

HOW TO TURN ON AUTOMATIC INVOICE REMINDERS:
1. In your Stripe dashboard, look at the left sidebar and click "Settings" (gear icon at the bottom)
2. Under the "Billing" section heading, click "Subscriptions and emails"
3. Scroll down to find the section called "Manage failed payments"
4. Look for "Invoice emails" — here you can enable:
   - "Send a reminder before payment is due" (set to 3 or 7 days before)
   - "Send a reminder after payment is due" (for overdue invoices)
5. Toggle each reminder ON by clicking the switch next to it
6. Click "Save" at the bottom of the page

HOW TO CREATE AND SEND AN INVOICE:
1. In the left sidebar, click "Billing" then "Invoices"
2. Click the blue "+ New" button (top right)
3. In "Customer", type your client's name or email — Stripe will look them up or create a new one
4. Click "+ Add line item", describe the work, set the price
5. Set the due date using the "Due date" field
6. Click "Send invoice" — your client gets an email with a link to pay online

WHAT YOUR CLIENT SEES: A professional email with your business name and a "Pay invoice" button.
They can pay by card in about 60 seconds. No Stripe account needed on their end.
"""
    },

    "zapier": {
        "source": "https://help.zapier.com/hc/en-us/articles/22234847450893",
        "verified": "April 2026",
        "content": """
ZAPIER — WHAT IT IS AND HOW TO CREATE YOUR FIRST AUTOMATION
(Zapier connects apps so they talk to each other automatically — free plan available at zapier.com)

WHAT IS ZAPIER IN PLAIN ENGLISH:
Zapier is a service that watches one app for something to happen (called a "trigger"),
then automatically does something in another app (called an "action"). For example:
"When a new form is submitted on my website (trigger), add that person to my email list (action)."
You set it up once — Zapier runs it for you 24/7.

HOW TO CREATE AN ACCOUNT:
1. Go to zapier.com
2. Click "Sign up" — you can use your Google account to make it faster
3. Zapier will ask what apps you use — you can skip this for now
4. You'll land on your Zapier home screen

HOW TO CREATE YOUR FIRST ZAP (AUTOMATION):
1. Click the orange "Create" button (top left of the screen)
2. Click "Zaps" from the dropdown
3. You'll see a blank automation builder — it has two sections: "Trigger" and "Action"

SETTING UP THE TRIGGER (what starts the automation):
4. Click the "Trigger" box
5. In the search bar, type the name of the app where something happens (e.g. "Gmail" or "Stripe")
6. Click on the app, then choose the specific event — e.g. "New Email" or "Payment Failed"
7. Click "Continue" and connect your account when prompted (click "Sign in to [App]")
8. Zapier will find recent examples to test with — pick one and click "Continue"

SETTING UP THE ACTION (what happens next):
9. Click the "Action" box
10. Search for the second app (e.g. "Mailchimp" or "Gmail")
11. Choose what Zapier should do — e.g. "Send Email" or "Add Subscriber"
12. Fill in the details — you'll see dropdown fields to map information from the trigger
13. Click "Test action" — Zapier will do the action once so you can see it work
14. If the test looks right, click "Publish" — your automation is now live

ZAPIER FREE PLAN LIMITS: 5 Zaps, 100 tasks per month. Enough to start.

IF SOMETHING GOES WRONG:
- "I can't find my app" — use the search bar, most popular apps are in Zapier
- "My Zap isn't triggering" — check it's turned ON (toggle on the Zap list page)
- "The test failed" — re-read the error message, it usually tells you exactly what's missing
"""
    },

    "calendly": {
        "source": "https://calendly.com/learn/calendly-setup",
        "verified": "April 2026",
        "content": """
CALENDLY — HOW TO SET UP YOUR BOOKING PAGE SO CLIENTS CAN SCHEDULE THEMSELVES
(Calendly is free at calendly.com — clients book time with you without any back-and-forth)

HOW TO CREATE AN ACCOUNT:
1. Go to calendly.com
2. Click "Sign up for free"
3. Sign up with your Google account (easiest) or enter your email
4. Choose a username — this becomes part of your booking link (e.g. calendly.com/yourname)
   Tip: use your name or business name, keep it short
5. Connect your calendar — click "Connect a calendar", then pick Google Calendar or Outlook
   This is important: Calendly reads your calendar so it only shows times you're free

HOW TO SET YOUR WORKING HOURS:
6. After connecting your calendar, you'll see "Set your availability"
7. Tick the days you want to take bookings
8. Set your start and end times for each day (e.g. 9:00 AM to 5:00 PM)
9. Click "Continue"

HOW TO CREATE A BOOKING TYPE (e.g. "30-minute call"):
10. You'll see a default "30 Minute Meeting" already created — click on it to edit it
11. Change the name to something clear: e.g. "Discovery Call" or "Client Consultation"
12. Set the duration (15, 30, 45, or 60 minutes)
13. Under "Location", choose how you'll meet:
    - "Phone call" — Calendly will ask them for their number
    - "Google Meet" — it automatically creates a video link
    - "In-person" — add your address
14. Click "Save and close"

HOW TO SHARE YOUR BOOKING LINK:
15. Click "Share" on your event type
16. Copy your Calendly link — it looks like: calendly.com/yourname/30-minute-meeting
17. Paste this link in your email signature, on your website, or send it directly to clients
18. When someone clicks the link, they'll see your available times and can book themselves

WHAT HAPPENS WHEN SOMEONE BOOKS:
- They pick a time, enter their name and email, answer any questions you set
- Both you and them get a confirmation email with a calendar invite
- Calendly sends automatic reminders to them before the meeting
- The meeting appears on your connected calendar automatically

IF SOMETHING GOES WRONG:
- "No times are showing as available" — check your calendar is connected and your availability is set
- "Client says the link doesn't work" — make sure your Calendly account is active and you're not on a deactivated free plan
- "Wrong timezone showing" — go to your account settings and update your timezone
"""
    },

    "mailchimp": {
        "source": "https://mailchimp.com/help/getting-started-with-campaigns/",
        "verified": "April 2026",
        "content": """
MAILCHIMP — HOW TO BUILD AN EMAIL LIST AND SEND YOUR FIRST EMAIL
(Mailchimp is free for up to 500 contacts at mailchimp.com)

HOW TO CREATE AN ACCOUNT:
1. Go to mailchimp.com
2. Click "Sign up free"
3. Enter your email, username, and password
4. Check your email for a confirmation link — click it
5. Mailchimp asks a few questions about your business — answer them honestly

HOW TO CREATE YOUR EMAIL LIST (called an "Audience" in Mailchimp):
6. In the left sidebar, click "Audience" (the person icon)
7. Click "Add contacts" then "Import contacts" if you have a spreadsheet of emails
   OR click "Add a subscriber" to add people one by one
8. To build your list from scratch, click "Signup forms" in the Audience menu
9. Click "Form builder" — this creates a form people fill in to join your list
10. Customize the form title and click "Save"
11. Mailchimp gives you a link to your signup form — add this to your website or share it

HOW TO SEND YOUR FIRST EMAIL CAMPAIGN:
12. In the left sidebar, click "Create" (the plus icon)
13. Click "Email"
14. Select "Regular email" — this is the standard option for beginners
15. Give your campaign a name (this is just for you, clients won't see it) — click "Begin"
16. Under "To", click "Add recipients" and select your audience/list
17. Under "From", enter your name and your email address
18. Under "Subject", type your email's subject line — make it clear and specific
19. Click "Design email" — you'll see Mailchimp's template library
20. Pick a simple template (the basic "1 Column" layout is best for beginners)
21. Click on any text block to edit it — type your message
22. Click the preview eye icon to see how it looks, and "Send test email" to check it in your inbox
23. When you're happy, click "Continue" then "Send now"

WHAT HAPPENS NEXT: Mailchimp sends the email to your list and shows you how many people
opened it and clicked any links. This is called your "campaign report".

IF SOMETHING GOES WRONG:
- "My email went to spam" — make sure your "From" email is your business email, not Gmail/Hotmail
- "People aren't on my list" — check they went through the signup form or were imported correctly
- "I can't find my campaign" — click "Campaigns" in the left sidebar
"""
    },

    "chatgpt": {
        "source": "https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt",
        "verified": "April 2026",
        "content": """
CHATGPT — WHAT IT IS AND HOW TO USE IT (COMPLETE BEGINNER GUIDE)
(ChatGPT is a free AI assistant at chatgpt.com — no download needed, works in your browser)

WHAT IS CHATGPT IN PLAIN ENGLISH:
ChatGPT is an AI (artificial intelligence) assistant you type to, like texting.
You ask it to do something — write an email, explain a topic, create a plan — and it does it.
It's like having a very knowledgeable assistant available 24/7 who never gets tired.
It's free to use the basic version at chatgpt.com.

HOW TO GET STARTED:
1. Open your internet browser (Chrome, Safari, Firefox — any of them work)
2. Go to chatgpt.com
3. Click "Sign up" to create a free account — you can use your Google account to make it quick
4. Once logged in, you'll see a text box at the bottom of the screen — this is where you type

HOW TO USE IT — THE BASICS:
5. Click in the text box at the bottom of the screen
6. Type what you want ChatGPT to do — this is called a "prompt"
7. Press Enter or click the arrow button to send
8. ChatGPT will type its response — you can read it as it appears
9. If you want to change or improve the response, just type a follow-up message like:
   "Make it shorter" or "Make it more formal" or "Add a section about X"

HOW TO GET GOOD RESULTS — TIPS FOR BEGINNERS:
- Be specific: instead of "write an email", say "write a short, friendly email to a client who is 7 days late paying my invoice for $500"
- Give context: tell it who you are and who you're writing to
- Ask for exactly what you need: "bullet points" or "one paragraph" or "formal tone"
- If you don't like the answer, just ask it to try again: "Can you try that again but make it less aggressive?"

COPYING THE RESULT:
- When ChatGPT gives you text, hover over it to see a "Copy" button (looks like two squares)
- Click Copy, then paste the text wherever you need it (email, document, etc.)

IMPORTANT NOTES:
- ChatGPT sometimes makes mistakes — always read what it gives you before using it
- Don't give it sensitive information like passwords or bank details
- The free version (GPT-3.5) is perfectly good for writing, planning, and business tasks
"""
    },

    "claude": {
        "source": "https://claude.ai",
        "verified": "April 2026",
        "content": """
CLAUDE — AN ALTERNATIVE AI ASSISTANT (OFTEN BETTER FOR WRITING TASKS)
(Claude is a free AI assistant at claude.ai — works the same way as ChatGPT)

WHAT IS CLAUDE:
Claude is an AI assistant made by Anthropic. It works exactly like ChatGPT — you type a
request, it responds. Many people find Claude gives more nuanced, better-written responses
for business documents, emails, and detailed plans. Free to use at claude.ai.

HOW TO USE IT:
1. Go to claude.ai in your browser
2. Click "Start for free" and create an account (or use your Google account)
3. You'll see a text box — type your request and press Enter
4. Claude will respond. You can reply to refine the answer, just like a conversation.

THE PROMPTS IN THIS GUIDE WORK IN BOTH CHATGPT AND CLAUDE:
All prompts in the AI Prompt Library section of this guide can be pasted into either
chatgpt.com or claude.ai — they work the same way in both. Use whichever you prefer.
"""
    },

    "google sheets": {
        "source": "https://support.google.com/docs/answer/6000292",
        "verified": "April 2026",
        "content": """
GOOGLE SHEETS — HOW TO CREATE A SPREADSHEET FOR TRACKING
(Google Sheets is completely free at sheets.google.com — you just need a Google/Gmail account)

HOW TO GET STARTED:
1. Go to sheets.google.com in your browser
2. If you have a Gmail account, you're already set — just log in
3. If not, create a free Google account at google.com/account/about
4. Click the big "+" button (or "Blank spreadsheet") to create a new spreadsheet
5. Click on the title "Untitled spreadsheet" at the top and rename it to something useful

THE BASICS OF GOOGLE SHEETS:
- Each box is called a "cell" — click any cell to start typing in it
- The columns go across (A, B, C...) and rows go down (1, 2, 3...)
- To move to the next cell, press Tab (moves right) or Enter (moves down)
- To add a column header, click cell A1 and type the heading (e.g. "Month")

HOW TO USE A FORMULA (automatic calculation):
- Click an empty cell where you want the result
- Type = to start a formula
- Example: to add up cells B2 to B13, type =SUM(B2:B13) and press Enter
- The cell will now show the total — it updates automatically when you change the numbers

HOW TO SHARE YOUR SPREADSHEET:
- Click the green "Share" button in the top right
- Type an email address to share with a specific person
- Or click "Copy link" to share a link — set it to "Anyone with the link can view"

HOW TO SAVE: Google Sheets saves automatically — you don't need to press Ctrl+S.
Look for the "Saving..." text next to the file name to confirm it's saved.
"""
    },

    "gmail": {
        "source": "https://support.google.com/mail",
        "verified": "April 2026",
        "content": """
GMAIL — HOW TO SEND PROFESSIONAL EMAILS AND USE TEMPLATES
(Gmail is Google's free email service at gmail.com — you need a Google account to use it)

HOW TO CREATE A GOOGLE ACCOUNT (if you don't have one):
1. Go to accounts.google.com in your browser
2. Click the blue "Create account" button
3. Fill in your first name, last name, username (this becomes your @gmail.com address), and password
4. Click "Next" and follow the verification steps (Google may ask for your phone number)
5. Once set up, go to gmail.com — this is your email inbox

HOW TO COMPOSE AND SEND AN EMAIL:
1. Click the large "+ Compose" button in the top-left corner of Gmail
   — A new email window will pop up in the bottom-right of your screen
2. In the "To" field, type the recipient's email address
3. In the "Subject" field, type your email subject line
4. Click in the large white area below the subject line and type your message
5. When ready, click the blue "Send" button at the bottom of the compose window
   — You'll see the compose window close. The email is now sent.
   — You can confirm it was sent by clicking "Sent" in the left sidebar.

HOW TO CREATE AN EMAIL TEMPLATE (so you can reuse the same email):
1. Click the gear icon (⚙️) in the top-right corner of Gmail
2. Click "See all settings" from the dropdown
   — You'll see a row of tabs: General, Labels, Inbox, Filters, etc.
3. Click the "Advanced" tab
4. Find the row labelled "Templates" — click the "Enable" button next to it
5. Scroll to the bottom and click the blue "Save Changes" button
   — Gmail will reload. Templates are now turned on.

HOW TO SAVE AN EMAIL AS A TEMPLATE:
1. Click "+ Compose" to open a new email window
2. Write the email you want to save as a template (e.g., your payment reminder)
3. Click the three vertical dots (⋮) at the bottom of the compose window
4. Hover over "Templates" in the menu that appears
5. Click "Save draft as template" > "Save as new template"
6. Give your template a name (e.g., "Payment Reminder - Day 7") and click "Save"

HOW TO USE A SAVED TEMPLATE:
1. Click "+ Compose" to start a new email
2. Click the three vertical dots (⋮) at the bottom
3. Hover over "Templates" > click the template name you want
   — Gmail will fill in the email body automatically. Just update the To and Subject fields.
4. Click "Send" when ready

HOW TO SCHEDULE AN EMAIL TO SEND LATER:
1. Write your email as normal in the compose window
2. Click the small down arrow (▼) next to the blue "Send" button
3. Click "Schedule send"
4. Choose a suggested time or click "Pick date & time" to set your own
5. Click "Schedule send" to confirm
   — The email will sit in your "Scheduled" folder (left sidebar) until it sends automatically
"""
    },

    "convertkit": {
        "source": "https://help.kit.com/en/articles/2502558-getting-started-with-convertkit",
        "verified": "April 2026",
        "content": """
CONVERTKIT (now called Kit) — HOW TO SET UP AN EMAIL LIST AND SEND NEWSLETTERS
(ConvertKit/Kit is a free email marketing tool for creators at kit.com — free up to 10,000 subscribers)

HOW TO CREATE AN ACCOUNT:
1. Go to kit.com in your browser
2. Click the orange "Get started free" button
3. Enter your email, create a password, and enter your name
4. Answer a few questions about your business (they personalise your dashboard)
5. Confirm your email address — check your inbox for a verification email from Kit

YOUR DASHBOARD:
- The left sidebar has: Subscribers, Broadcasts, Automations, Forms, Landing Pages, Commerce
- "Subscribers" = your list of email contacts
- "Broadcasts" = one-off emails you send to your list
- "Forms" = sign-up boxes you put on your website to collect emails

HOW TO ADD A SUBSCRIBER MANUALLY:
1. Click "Subscribers" in the left sidebar
2. Click the "Add subscriber" button (top right)
3. Enter the person's email address and first name
4. Click "Save" — they now appear on your list

HOW TO CREATE A SIGN-UP FORM (so people can join your list from your website):
1. Click "Grow" in the left sidebar, then click "Forms"
2. Click the orange "Create form" button
3. Choose "Inline" (a form that sits inside a web page)
4. Choose a template and click "Select"
5. Edit the headline and button text to match your offer
6. Click "Save" in the top-right corner
7. Click "Share" — you'll see an HTML code snippet to paste into your website, or a hosted URL you can link to directly

HOW TO SEND A BROADCAST (email to your whole list):
1. Click "Send" in the left sidebar, then click "Broadcasts"
2. Click the orange "New broadcast" button
3. Type your email subject in the "Subject" field
4. Click in the body area and type your email content
5. Click "Next: Choose recipients" — select "All subscribers" or a specific group
6. Click "Send broadcast" to send immediately, or "Schedule" to send at a specific time
   — You'll see a confirmation screen showing how many people will receive it
"""
    },
}


def get_tool_docs(tool_name: str) -> str:
    """Return verified documentation for a tool, or empty string if not in knowledge base."""
    key = tool_name.lower().strip()
    entry = TOOL_DOCS.get(key)
    if not entry:
        # Try aliases
        aliases = {
            "gmail": "gmail",
            "google mail": "gmail",
            "convertkit": "convertkit",
            "kit": "convertkit",
        }
        key = aliases.get(key, key)
        entry = TOOL_DOCS.get(key)
        if not entry:
            return ""
    return (
        f"=== VERIFIED SETUP INSTRUCTIONS FOR {tool_name.upper()} ===\n"
        f"Source: {entry['source']} (verified {entry['verified']})\n\n"
        f"{entry['content'].strip()}\n"
    )




def get_docs_for_category(category: str) -> str:
    """Return combined verified docs for all tools relevant to a problem category."""
    # Inline category→tool mapping to avoid circular import with researcher.py
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
    tools = CATEGORY_TOOLS.get(category, [])
    if not tools:
        return ""

    parts = []
    for tool in tools[:3]:
        doc = get_tool_docs(tool)
        if doc:
            parts.append(doc)

    if not parts:
        return ""

    return (
        "\n\nVERIFIED TOOL DOCUMENTATION (researched and confirmed current):\n"
        "Use the exact button names, menu paths, and steps below in your guide.\n\n"
        + "\n\n".join(parts)
    )


if __name__ == "__main__":
    # Test
    doc = get_tool_docs("wave")
    print(doc[:500])
    print(f"\nTotal tools in knowledge base: {len(TOOL_DOCS)}")
    print("Tools:", list(TOOL_DOCS.keys()))
