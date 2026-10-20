"""Task 1.7: AI model router.

Asks for a task type (code, private or chat) and the estimated tokens, then
picks the model: private data stays on a local model, code goes to a strong
cloud model, and everything else goes to a cheap one. Prints a length
warning and the estimated cost. Prices are EXAMPLES, not real quotes.
Stretch: free users sending more than 2000 tokens are asked to upgrade.
"""

# Why: strip() and lower() mean " Code " and "CODE" both work, so a typo in
# capitals or spaces doesn't send the request to the wrong model.
task = input("Task (code / private / chat): ").strip().lower()
tokens = int(input("Estimated tokens: "))
is_paid = input("Is this a paid user? (yes/no): ").strip().lower() == "yes"

# Why: if/elif/else checks the most specific cases first and lets "else"
# catch everything remaining, so every request always gets a model.
if task == "code":
    model = "claude (cloud, strong at code)"
    price = 0.8   # example PKR per 1K tokens
elif task == "private":
    model = "llama3.2 (local, Ollama)"
    price = 0     # Why: a local model runs on our own machine, so no per-token fee
else:
    model = "gpt-mini (cloud, cheap chat)"
    price = 0.1   # example PKR per 1K tokens

cost = tokens / 1000 * price

if tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

# Stretch: both conditions must be true for the upgrade message.
if not is_paid and tokens > 2000:
    print("Upgrade to send long requests.")

print(f"Chosen model: {model}")
print(f"Estimated cost: {cost:.2f} PKR")