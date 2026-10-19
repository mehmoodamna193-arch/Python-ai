"""Task 1.5: AI Model Profile Card.

Stores a profile of one AI model using the four basic types (str, int,
float, bool), prints each value with its type, then asks how many tokens a
chat uses and prints the estimated cost per chat in PKR.
The price is an EXAMPLE only, not a real quote.
Stretch: also estimates the monthly cost from chats per day (30 days).
"""

# Why: each value is a different type, so we can see how Python tells
# text, whole numbers, decimals and True/False apart with type().
model_name = "llama3.2"        # str
context_window = 128000        # int: max tokens the model can hold at once
price_per_1k_tokens = 0.5      # float: EXAMPLE price in PKR, not a real quote
runs_locally = True            # bool

print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window} tokens {type(context_window)}")
print(f"Price per 1K tokens: {price_per_1k_tokens} PKR {type(price_per_1k_tokens)} (example price)")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# Why: input() always returns text, so int() converts it to a number we can
# do maths with; without it, multiplying would fail or repeat the string.
tokens_per_chat = int(input("\nHow many tokens does one chat use? "))

# Why: prices are quoted per 1,000 tokens, so divide by 1000 first; round()
# keeps the result to 2 decimals, which is how money is normally shown.
cost_per_chat = round(tokens_per_chat / 1000 * price_per_1k_tokens, 2)

print(f"Tokens per chat: {tokens_per_chat}")
print(f"Estimated cost: {cost_per_chat} PKR")

# Stretch: scale the per-chat cost up to a 30-day month.
chats_per_day = int(input("\nHow many chats per day? "))
monthly_cost = round(cost_per_chat * chats_per_day * 30, 2)
print(f"Estimated monthly cost (30 days): {monthly_cost} PKR")