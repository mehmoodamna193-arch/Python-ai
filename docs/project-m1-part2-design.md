# Project M1 Part 2: Sweet Crumbs Front Desk (design)

Business: Sweet Crumbs bakery (example data). All prices, hours and the address are examples.

## Intents

Rules are checked top to bottom. Order matters, so it was chosen on purpose.

| # | Intent | Keywords | Reply |
|---|--------|----------|-------|
| 1 | Bye | exact `bye` | Goodbye + session report |
| 2 | Complaint (first) | ` late`, `refund`, `complaint` | A manager will call you within 1 hour |
| 3 | Human handover | `human`, `agent` | Connecting you to a human... (chat ends) |
| 4 | Greeting | `==` `hi`, or starts with `hi `, `hello`, `salam`, `hey` | Hello, {name}! Ask about hours, delivery or prices |
| 5 | Quote | exact `/quote` | Asks item and quantity, prints the price breakdown |
| 6 | Hours | `hours`, `open`, `timing`, `closing` | Open 9 am to 10 pm, every day |
| 7 | Delivery | `deliver` | 200 PKR, free from 3,000 PKR after discount |
| 8 | Location | `where`, `location` | Shop 4, Main Market |
| 9 | Prices | `price`, `how much`, `cost`, ` fee` | Lists the three item prices |
| 10 | Fallback | anything else | Counted as unanswered, routed, AI prompt printed |

Why this order:
- Complaint is before everything, so an unhappy customer always reaches a human.
- Greeting uses `==` / `.startswith()`, never `in`, because `hi` hides inside "which" and "this".
- ` late` and ` fee` start with a space so "choco**late**" and "cof**fee**" do not match.
- Delivery is checked before Prices, so "how much is delivery" gets the delivery answer.

## Business rules

| Rule | Value |
|------|-------|
| Item prices | cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR |
| Bulk discount | 10% off for 10 or more items |
| Delivery | 200 PKR, free when the total after discount is 3,000 PKR or more |
| Private words | phone, cnic, address |
| Cloud price (example) | 0.1 PKR per 1K tokens; local model 0 PKR |
| Max question length | 150 characters |

Rule order for a quote: price x quantity = subtotal, then the discount, then the delivery check on the discounted amount. Example: 12 cupcakes = 3,000, minus 10% = 2,700, which is below 3,000, so delivery (200) is still charged. Total 2,900.

How the report counts: Messages = every non-empty message including `bye` and `/quote`. Answered by rules = FAQ, greeting and complaint replies (quotes are counted separately). Unanswered = fallback questions.

## Rule tests

| # | You type | Expected | Actual | Pass? |
|---|----------|----------|--------|-------|
| 1 | ` WHAT are your hours ` | Hours | "We are open 9 am to 10 pm, every day." | Pass |
| 2 | `which cake is best?` | Fallback, not a greeting | Routed to cloud model, prompt printed | Pass |
| 3 | `my order is late` | Manager reply | "A manager will call you within 1 hour." | Pass |
| 4 | `/quote`, chocolate cake, 1 | Delivery fee charged | 1,500 + 200 delivery = 1,700 PKR | Pass |
| 5 | `/quote`, chocolate cake, 3 | Delivery free | 4,500 PKR, delivery 0 | Pass |
| 6 | `/quote`, brownie, 10 | Discount applied | 3,000, discount -300, delivery 200, total 2,900 | Pass |
| 7 | `/quote`, pizza, 2 | "Not on our menu", no crash | "Sorry, pizza is not on our menu." | Pass |
| 8 | `how do I give my CNIC?` | Local model, cost 0 | llama3.2 (local, private), report shows 0.0000 PKR | Pass |
| 9 | Press Enter with no text | Asks again | "Please type your question." and not counted | Pass |
| 10 | `BYE` | Goodbye + report | Goodbye and report printed | Pass |

Extra tests I added:

| You type | Expected | Result | Pass? |
|----------|----------|--------|-------|
| `chocolate cake price` | Prices, not a complaint ("choco**late**" trap) | Price list | Pass |
| `/quote`, cupcake, `abc` | Polite message, no crash (bonus) | "Please type the quantity as a whole number" | Pass |
| `I want a human` | Handover, chat ends, report still prints | "Connecting you to a human..." then report | Pass |
| `  HI ` then `hi there` | Greeting both times | Greeting both times | Pass |
| `/quote`, chocolate cake, 10 | Discount and free delivery | 15,000 - 1,500 = 13,500, delivery 0 | Pass |