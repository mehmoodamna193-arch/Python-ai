"""Module 1 Project: Sweet Crumbs bakery front desk.

What it does: a chat front desk for a local bakery.
  1. Answers common questions (hours, location, delivery, prices) with rules, for free.
  2. Gives exact price quotes with a bulk discount and a delivery fee (/quote).
  3. For anything else, cleans and shortens the question, estimates tokens,
     routes it (private -> local model, otherwise cheap cloud model) and
     prints an AI-ready prompt.
  4. Ends with a session report the owner can act on.

Business: Sweet Crumbs bakery (example data - change it for a real client).
Only Module 1 tools are used: no lists, dictionaries, for loops or functions.
"""

# Why: constants in UPPER_CASE sit at the top so the owner's numbers can be
# changed in one place without hunting through the logic.
BOT_NAME = "Sweet Crumbs Desk"
BUSINESS = "Sweet Crumbs bakery"
DELIVERY_FEE = 200            # PKR
FREE_DELIVERY_LIMIT = 3000    # PKR, checked AFTER the discount
CLOUD_PRICE_PER_1K = 0.1      # PKR per 1K tokens, EXAMPLE price, not a real quote
BULK_MIN_QUANTITY = 10
BULK_DISCOUNT_PERCENT = 10
CUPCAKE_PRICE = 250
BROWNIE_PRICE = 300
CHOCOLATE_CAKE_PRICE = 1500
MAX_QUESTION_LENGTH = 150

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

# Why: the name is asked once, before the loop, so every later reply can use
# it without asking again.
name = input(f"{BOT_NAME}: What is your name? ").strip().title()
if name == "":
    name = "Friend"

message_count = 0
rule_answers = 0
unanswered_count = 0
quote_count = 0
quoted_value = 0
complaint_count = 0
total_ai_cost = 0.0

while True:
    # Why: strip() + lower() make " WHAT are your HOURS " match "hours",
    # so customers' random capitals and spaces never break a rule.
    message = input(f"{name}: ").strip().lower()

    # Why: an empty message is not a question; asking again keeps it out of
    # the counts and stops an empty prompt being sent to an AI.
    if message == "":
        print(f"{BOT_NAME}: Please type your question.")
        continue

    message_count += 1

    if message == "bye":
        print(f"{BOT_NAME}: Goodbye, {name}!")
        break

    # Why: the complaint rule is FIRST, so an unhappy customer never gets a
    # cheerful canned answer (e.g. "my chocolate order is late" must not hit
    # the price rule). " late" has a leading space so "chocolate" can't match.
    elif " late" in message or message.startswith("late") or "refund" in message or "complaint" in message:
        complaint_count += 1
        rule_answers += 1
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")

    # Bonus: a human keyword ends the chat; the report still prints below.
    elif "human" in message or message == "agent" or " agent" in message:
        print(f"{BOT_NAME}: Connecting you to a human...")
        break

    # Why: greetings use == / startswith, never `in`, because "hi" hides
    # inside words like "which" and "this" and would wrongly match them.
    elif message == "hi" or message.startswith("hi ") or message.startswith("hello") or message.startswith("salam") or message.startswith("hey"):
        rule_answers += 1
        print(f"{BOT_NAME}: Hello, {name}! Ask about hours, delivery or prices, or type /quote.")

    elif message == "/quote":
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # Bonus: .isdigit() is checked BEFORE int(), so typing letters gives a
        # polite reply instead of a ValueError crash.
        if not quantity_text.isdigit() or quantity_text == "0":
            print(f"{BOT_NAME}: Please type the quantity as a whole number, like 12.")
        else:
            quantity = int(quantity_text)

            if item == "cupcake":
                unit_price = CUPCAKE_PRICE
            elif item == "brownie":
                unit_price = BROWNIE_PRICE
            elif item == "chocolate cake":
                unit_price = CHOCOLATE_CAKE_PRICE
            else:
                unit_price = 0

            if unit_price == 0:
                print(f"{BOT_NAME}: Sorry, {item} is not on our menu.")
            else:
                subtotal = quantity * unit_price

                # Why: the discount is applied BEFORE the delivery check, so
                # the free-delivery limit is tested on what the customer really
                # pays. 12 cupcakes = 3,000, minus 10% = 2,700, which is under
                # the limit, so delivery is still charged.
                if quantity >= BULK_MIN_QUANTITY:
                    discount = round(subtotal * BULK_DISCOUNT_PERCENT / 100)
                else:
                    discount = 0
                after_discount = subtotal - discount

                if after_discount >= FREE_DELIVERY_LIMIT:
                    delivery = 0
                else:
                    delivery = DELIVERY_FEE

                total = after_discount + delivery
                quote_count += 1
                quoted_value += total

                print(f"{BOT_NAME}: {quantity} x {item} = {subtotal:,} PKR")
                if discount > 0:
                    discount_text = f"-{discount:,}"
                else:
                    discount_text = "0"
                print(f"     Discount: {discount_text} PKR | Delivery: {delivery:,} PKR")
                print(f"     Total: {total:,} PKR")

    elif "hours" in message or "open" in message or "timing" in message or "closing" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: We are open 9 am to 10 pm, every day.")

    elif "deliver" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: Delivery is {DELIVERY_FEE:,} PKR, free for orders of {FREE_DELIVERY_LIMIT:,} PKR or more after discount.")

    elif "where" in message or "location" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: We are at Shop 4, Main Market.")

    # Why: " fee" has a leading space so "coffee" can't trigger the price rule.
    elif "price" in message or "how much" in message or "cost" in message or " fee" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: Cupcake {CUPCAKE_PRICE} PKR, brownie {BROWNIE_PRICE} PKR, chocolate cake {CHOCOLATE_CAKE_PRICE:,} PKR. Type /quote for an exact total.")

    else:
        # Smart fallback: clean, cut to 150 characters, estimate tokens, route.
        unanswered_count += 1
        question = message.capitalize()[:MAX_QUESTION_LENGTH]
        estimated_tokens = round(len(question) / 4)

        # Why: private details (phone, CNIC, address) must never leave our
        # machine, so they go to a local model that costs nothing per token.
        if "phone" in message or "cnic" in message or "address" in message:
            model = "llama3.2 (local, private)"
            ai_cost = 0
        else:
            model = "small cloud model (cheap)"
            ai_cost = estimated_tokens / 1000 * CLOUD_PRICE_PER_1K
        total_ai_cost += ai_cost

        prompt = f"""You are the assistant of {BUSINESS}.
Answer {name} in 2 short lines.
Question: {question}"""

        print(f"{BOT_NAME}: Good question! Routed to: {model} (~{estimated_tokens} tokens)")
        print("     Prompt:")
        print(prompt)

print("=" * 50)
print("Session report")
print(f"Messages: {message_count} | Answered by rules: {rule_answers} | Unanswered: {unanswered_count}")
print(f"Quotes: {quote_count} | Quoted value: {quoted_value:,} PKR")
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print(f"Complaints: {complaint_count}")
print("=" * 50)