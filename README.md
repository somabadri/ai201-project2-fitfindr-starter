# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory

Your README submission must document each tool's name, inputs, and return value. **These must exactly match your actual function signatures in `tools.py`.** Your documented interfaces will be checked against your actual function signatures in `tools.py` — if the parameter count or types contradict what's in the code, you may not receive full credit for that tool.

### `search_listings(description, size, max_price)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `description` | `str` | Keywords describing what the user is looking for (e.g. `"vintage graphic tee"`) |
| `size` | `str \| None` | Size string to filter by, or `None` to skip size filtering. Case-insensitive — `"M"` matches `"S/M"` |
| `max_price` | `float \| None` | Maximum price (inclusive), or `None` to skip price filtering |

**Returns:** `list[dict]` — matching listing dicts sorted by keyword relevance, best match first. Returns an empty list if nothing matches.

---

### `suggest_outfit(new_item, wardrobe)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `new_item` | `dict` | A listing dict for the item the user is considering buying |
| `wardrobe` | `dict` | A wardrobe dict with an `items` key containing a list of wardrobe item dicts. May be empty |

**Returns:** `str` — 1–2 outfit suggestions as a non-empty string. If the wardrobe is empty, returns general styling advice instead of wardrobe-specific pairings.

---

### `create_fit_card(outfit, new_item)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `outfit` | `str` | The outfit suggestion string returned by `suggest_outfit()` |
| `new_item` | `dict` | The listing dict for the thrifted item |

**Returns:** `str` — a 2–4 sentence Instagram/TikTok-style caption mentioning the item name, price, and platform. If `outfit` is empty or whitespace-only, returns a descriptive error message string instead of raising an exception.

---

## Planning Loop and State Management

`run_agent()` in `agent.py` orchestrates the three tools sequentially using a single session dict as the source of truth. On each call, it initializes the session with the user's query and wardrobe, then uses regex to parse a clean description, optional size, and optional price ceiling from the raw query. It calls `search_listings()` first and stores the results in `session["search_results"]` — if the list is empty, it writes a user-facing message to `session["error"]` and returns immediately without calling the remaining tools. Otherwise it picks `results[0]` as `session["selected_item"]` and passes it directly into `suggest_outfit()`, storing the string response in `session["outfit_suggestion"]`. That string and the selected item are then passed into `create_fit_card()`, with the caption stored in `session["fit_card"]`. Every value travels through the session dict — no tool re-parses the query or re-fetches the listing, so the same item dict is guaranteed to flow through all three steps unchanged.

---

## Interaction Walkthrough

<!-- Walk through a complete interaction step by step: natural language query → each tool call (and why) → final fit card.
     Walk through this carefully — it's how graders follow your agent's reasoning without a live demo.
     Use a specific example — do not leave this as a template. -->
**User query:** I want to wear a track jacket.

**Step 1 — Tool called:**
- Tool: search_listings()
- Input: I want to wear a track jacket.
- Why this tool: It's the first step to check to find which listings are relevant.
- Output: 
```
90s Track Jacket — Navy/White Stripe
Price:     $45.00
Size:      M
Condition: excellent
Platform:  poshmark
Tags:      90s, vintage, athletic, streetwear

Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.
```

**Step 2 — Tool called:**
- Tool: suggest_outfit()
- Input: The item from above
- Why this tool: It's going to use the existing wardrobe and suggest outfits based on the input.
- Output: 

```
Here are 2 specific outfit combinations using the 90s Track Jacket and pieces from their wardrobe:

1. **Casual Streetwear**: Pair the 90s Track Jacket with the Baggy straight-leg jeans, White ribbed tank top, and Chunky white sneakers. This outfit combines the athletic and streetwear styles, creating a relaxed and casual look.

2. **Vintage Athletic**: Combine the 90s Track Jacket with the Black cropped zip hoodie, Wide-leg khaki trousers, and Black combat boots. This outfit blends vintage and athletic elements, adding a touch of earthy tones with the khaki trousers, and creating a unique, layered look.
```

**Step 3 — Tool called:**
- Tool: create_fit_card()
- Input: The suggestion from the step above and the item from step one.
- Why this tool: It creates a sharable caption for the outfit.
- Output: 
```
I'm obsessed with my new 90s Track Jacket that I scored for $45 on Poshmark, and I've been experimenting with different ways to style it. My favorite combo so far is pairing it with baggy straight-leg jeans, a white ribbed tank top, and chunky white sneakers for a super casual, streetwear-inspired look. There's something about the navy and white stripes that just screams vintage athleticism, and I love how it adds a cool, laid-back vibe to my outfit. I feel like I can throw this on and head out the door, knowing I'm rocking a relaxed, sporty style.
```

**Final output to user:**
```
I'm obsessed with my new 90s Track Jacket that I scored for $45 on Poshmark, and I've been experimenting with different ways to style it. My favorite combo so far is pairing it with baggy straight-leg jeans, a white ribbed tank top, and chunky white sneakers for a super casual, streetwear-inspired look. There's something about the navy and white stripes that just screams vintage athleticism, and I love how it adds a cool, laid-back vibe to my outfit. I feel like I can throw this on and head out the door, knowing I'm rocking a relaxed, sporty style.
```
---

## Error Handling and Fail Points

<!-- For each tool, describe the specific failure mode and what your agent does in response.
     This maps to the error handling section of the rubric (F5-C1). -->

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| `search_listings` | No listings match the description, size, or price filters | Returns an empty list; `run_agent` sets `session["error"]` with a message asking the user to broaden their search, and exits before calling `suggest_outfit` |
| `suggest_outfit` | Wardrobe `items` list is empty (new user) | Skips wardrobe-specific pairing and prompts the LLM for general styling advice instead; always returns a non-empty string |
| `create_fit_card` | `outfit` argument is empty or whitespace-only | Returns a descriptive error message string without calling the LLM and without raising an exception |

---

## Spec Reflection

<!-- Answer both questions with at least 2–3 sentences each. -->

**One way planning.md helped during implementation:**
It allowed me to structure my prompts to Claude in a digestible manner and implement the tools iteratively. Given the prior planning, I was able to assess each step properly because I knew what the inputs and outputs should be at every step.


**One divergence from your spec, and why:**
The one place I diverged from the spec was how verbose all the LLM responses were compared to what I anticipated. I think I need to include length limits within the prompt to have it return what I anticipated, but the verbose results lead to overall better final result.
---

## AI Usage
I provided the Claude with all of my planning.md and asked it to ingest the file into the context. This gave it all the instructions it needed to be helpful. I then was able to take each step and provide it instructions for implementation. The one place I had to question the AI was regarding how it implemented the sorting in Step 1. I asked it to explain the code and consider tradeoffs. I ended up only making a small tweak but keeping the majority of the logic.

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
