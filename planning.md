# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This function takes in an user query, and additional information such as size and max price and it returns listings.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): This is the description from the user query.
- `size` (str): This is the size of the clothing described in the user query.
- `max_price` (float): This is the max price describe in the user query.

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
It returns a list of items matching the criteria mentioned in the user query ordered by relevancy.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
The agent should recognize that nothing was returned and let the user know that no listings were found matching that criteria and ask them to try again with less restrictions.
---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
It takes in the new item found in the listings from search_listings and the user's current wardrobe and returns suggestions.
**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): It's the item returned from search_listings based on the user's query.
- `wardrobe` (dict): It's the user's current wardrobe.

**What it returns:**
<!-- Describe the return value -->
It's returns an outfit suggestion with the new item and items in the wardrobe.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
The agent should recognize that nothing was returned and let the user know that no outfit suggestions could be created.
---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
It creates a description of the outfit mentioning the new item and where it's from and the existing item in the wardrobe.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (str): It's the suggestion from suggest_outfit
- `new_item` (dict): the new item from search_listings

**What it returns:**
<!-- Describe the return value -->
It returns a str which mentions the new item, where it's from and the existing wardrobe piece.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
The agent should recognize that nothing was returned and let the user know that a fit card wasn't able to be created.
---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
After search_listings runs, check if results is empty. If yes, set an error message stating that a listing wasn't found in the session and return early. If no, set selected_item = results[0] and proceed to suggest_outfit. After suggest_outfit runs, check if results is empty. If yes, set an error message stating that an outfit suggestion wasn't able to be created in the session and return early. If no, set outfit = result and proceed to create_fit_card. After create_fit_card runs, check if result is empty. If yes, set an error message stating that an fit card wasn't able to be created, otherwise return the result.
---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

The agent will have access to the a global state where new_item, wardrobe, outfit, and error are tracked.

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | Ask the user to try again with less restrictions because no matches were found. |
| suggest_outfit | Wardrobe is empty | Tell the user there are no items in wardrobe and if they want suggestions for a whole outfit instead. |
| create_fit_card | Outfit input is missing or incomplete | Ask the user if they want another outfit suggestion to create a fit card.|

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     Use ASCII art or a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html).
     Do NOT embed an image — graders need to read your diagram directly in the file;
     an embedded image or screenshot cannot be evaluated.
     You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

User query                                                                                                                       
    │                                                                                                                            
    ▼                                                                                                                            
Planning Loop ───────────────────────────────────────────┐                                                                       
    │                                                    │                                                                       
    ├─► search_listings(description, size, max_price)    │                                                                       
    │       │ results=[]                                 │                                                                       
    │       ├──► [ERROR] "No listings found..." → return │                                                                       
    │       │                                            │                                                                       
    │       │ results=[item, ...]                        │                                                                       
    │       ▼                                            │                                                                       
    │   Session: selected_item = results[0]              │                                                                       
    │       │                                            │                                                                       
    ├─► suggest_outfit(selected_item, wardrobe)          │                                                                       
    │       │                                            │                                                                       
    │   Session: outfit_suggestion = "..."               │                                                                       
    │       │                                            │                                                                       
    └─► create_fit_card(outfit_suggestion, selected_item)│                                                                       
            │                                            │                                                                       
        Session: fit_card = "..."                        │                                                                       
            │                                            └─Ask the user if they want to retry for an item with less restrictions.
            ▼                                                                                                                    
        Return session                                                                                                           
---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**
I will give Claude code my planning.md, describe the existing infrastructure (helper functions etc). Ask it to implement each function step by step and validate each function before moving forward.

**Milestone 4 — Planning loop and state management:**
I will Claude code my planning.md, ask it provide feedback on my plan, and consider trade offs before asking it to implement the loop and state management.
---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

FitFindr first uses search_listings() to find articles of clothing based on the user's query. It then takes the top result of those results and uses suggest_outfit() suggest a new outfit with the newly found article of clothing and the user's existing wardrobe. Finally, it takes the outfit and new item and creates a description using create_fit_card().


**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->
Call search_listings("vintage graphic tee", max_price=30)

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->
It will this listing: Vintage Band Tee — Faded Grey or something similar as new_item.  It will then call suggest_outfit using the listing dict and the user's wardrobe. A suggestion will be returned.

**Step 3:**
<!-- Continue until the full interaction is complete -->
It will call create_fit_card using the new_item and the suggestion from step 2. This will then return a fit card description.

**Final output to user:**
<!-- What does the user actually see at the end? -->
The user then gets the description.