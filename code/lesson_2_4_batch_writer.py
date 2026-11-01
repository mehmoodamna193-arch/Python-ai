"""Task 2.4: Batch Product Writer.

Loops over a dictionary of products, asks a local Ollama model (through
LangChain) for a one-sentence menu description of each one, and collects the
results in a list of dictionaries. Items with price 0 are skipped without
calling the AI. At the end it prints a numbered menu and a summary with the
total tokens and total seconds.
"""

from langchain.chat_models import init_chat_model

# Replace these with the products or services of your own business.
products = {
    "Old Stock": 0,
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
    "Fruit Tart": 450,
}

SYSTEM = (
    "You write menu descriptions for Sweet Crumbs bakery in Lahore. "
    "Reply with exactly one sentence. Do not mention the price. No quotes."
)

# Why create the model once, before the loop: loading it takes time, so every
# item reuses the same connection instead of paying that cost again.
# Why temperature 0.7: menu descriptions are creative, so some variety is good.
llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.7)

# Why start the accumulators at 0 before the loop: if they were set inside it,
# every item would reset them and we would only count the last one.
total_tokens = 0
total_seconds = 0
results = []  # Why a list: we print the menu after the loop, so we must store each answer

for name, price in products.items():
    if price == 0:
        # Why continue: a free or unpriced item needs no description, so skip
        # it before the AI call and spend no tokens or time on it.
        print(f"Skipping {name.lower()} (no price)")
        continue

    response = llm.invoke([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Write a description for: {name}"},
    ])

    total_tokens += response.usage_metadata["total_tokens"]
    # total_duration is in nanoseconds, so divide to get seconds
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

    results.append({"item": name, "price": price, "text": response.text.strip()})

print("=" * 50)
for number, result in enumerate(results, start=1):
    print(f"{number}. {result['item']} ({result['price']} PKR)")
    print(f"   {result['text']}")
print("=" * 50)
print(f"{len(results)} descriptions, {total_tokens} tokens, {total_seconds:.1f} seconds")