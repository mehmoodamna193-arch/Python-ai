"""Module 2 project: AI Content Studio for Sweet Crumbs bakery, Lahore.

A command-line studio for a local business owner. It writes menu
descriptions in one batch (/menu), writes social media posts in a chosen
tone and streams them word by word (/post), answers prices straight from a
dictionary with no AI (/price), and chats with customers using memory and
only real facts. When you type bye, it prints a session report with the
number of AI jobs, the tokens used and the AI time.
"""

from langchain.chat_models import init_chat_model

# Why a config dictionary: model name, memory size and temperatures sit in one
# place, so the owner's developer can change them without touching the logic.
config = {
    "model": "llama3.2",
    "max_messages": 8,
    "precise_temperature": 0.2,
    "creative_temperature": 0.8,
}

# Why facts in a dictionary: the owner's fear is invented prices, so every fact
# the AI may use lives here. A price of 0 means "coming soon".
# Replace these with the details of your own business.
facts = {
    "name": "Sweet Crumbs",
    "type": "bakery",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "delivery": "200 PKR, free for orders from 3000 PKR",
    "prices": {
        "mango tart": 0,
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
    },
}

tones = {
    "fun": "playful and full of energy, short sentences",
    "premium": "elegant and calm, focused on quality",
    "urgent": "exciting, limited-time feel, tells people to order today",
}

# Why two models: facts and customer chat need focused, repeatable answers
# (low temperature), while menu text and posts need variety (high temperature).
precise = init_chat_model(
    config["model"], model_provider="ollama", temperature=config["precise_temperature"]
)
creative = init_chat_model(
    config["model"], model_provider="ollama", temperature=config["creative_temperature"]
)

# Why only these facts: the system message is the AI's whole knowledge of the
# business, and we tell it to admit when it does not know instead of guessing.
system_message = (
    f"You are the assistant of {facts['name']}, a {facts['type']} in {facts['city']}. "
    f"Opening hours: {facts['hours']}. Delivery: {facts['delivery']}. "
    f"Prices in PKR: {facts['prices']}. A price of 0 means the item is coming soon "
    f"and cannot be ordered yet. Only use these facts. If the answer is not in "
    f"these facts, say you do not know. Never invent prices or products. "
    f"Answer in 2 short lines."
)

messages = [{"role": "system", "content": system_message}]

# Session counters. Why they start at 0 before the loop: if they were set
# inside it, every command would reset them and the report would be wrong.
chat_answers = 0
menu_descriptions = 0
posts = 0
price_answers = 0
total_tokens = 0
total_seconds = 0

print("=" * 50)
print(f"   {facts['name']} AI Content Studio")
print("=" * 50)
print(f"Commands: /menu, /post {'|'.join(tones)}, /price <item>, /reset, bye")

while True:
    text = input("You: ").strip()
    command = text.lower().split(" ")[0]  # first word, so capitals never matter
    argument = text[len(command):].strip().lower()  # everything after it

    if text == "":
        print("Studio: Please type a command or a question.")
    elif text.lower() == "bye":
        print("Studio: Goodbye!")
        break
    elif command == "/menu":
        results = []
        print("-" * 50)
        for item, price in facts["prices"].items():
            if price == 0:
                # Why continue: a coming-soon item has nothing to sell yet, so
                # we skip it before the AI call and spend no tokens on it.
                print(f"Studio: Skipping {item} (coming soon)")
                continue

            response = creative.invoke([
                {
                    "role": "system",
                    "content": (
                        f"You write menu descriptions for {facts['name']}, a "
                        f"{facts['type']} in {facts['city']}. Reply with exactly "
                        f"one sentence. Do not mention the price. No quotes."
                    ),
                },
                {"role": "user", "content": f"Write a description for: {item}"},
            ])

            menu_descriptions += 1
            total_tokens += response.usage_metadata["total_tokens"]
            # total_duration is in nanoseconds, so divide to get seconds
            total_seconds += response.response_metadata["total_duration"] / 1_000_000_000
            results.append({"item": item, "price": price, "text": response.text.strip()})

        for number, result in enumerate(results, start=1):
            print(f"{number}. {result['item'].title()} ({result['price']:,} PKR)")
            print(f"   {result['text']}")
        print("-" * 50)
    elif command == "/post":
        # Why .get() with a default: a wrong tone like "pirate" would crash
        # with a KeyError using tones[argument]; .get() falls back to "fun".
        tone_description = tones.get(argument, tones["fun"])
        print(f"Studio ({tone_description}):")

        last_chunk = None
        for chunk in creative.stream([
            {
                "role": "system",
                "content": (
                    f"You write short Instagram posts for {facts['name']}, a "
                    f"{facts['type']} in {facts['city']}. Tone: {tone_description}. "
                    f"Only use these facts: {facts}. Write at most 4 short lines."
                ),
            },
            {"role": "user", "content": "Write one post about one of our products."},
        ]):
            print(chunk.text, end="", flush=True)  # word by word, like ChatGPT
            last_chunk = chunk
        print()

        posts += 1
        # Why read the last chunk: Ollama sends the token and time numbers
        # only in the final chunk of a stream.
        if last_chunk is not None and last_chunk.usage_metadata:
            total_tokens += last_chunk.usage_metadata["total_tokens"]
            total_seconds += last_chunk.response_metadata.get("total_duration", 0) / 1_000_000_000
    elif command == "/price":
        # Why no AI here: a dictionary lookup is free, instant and always
        # correct, so a price can never be invented.
        if argument == "":
            print("Studio: Please type an item, for example /price cupcake")
        elif argument in facts["prices"]:
            price_answers += 1
            if facts["prices"][argument] == 0:
                print(f"Studio: {argument.title()} is coming soon.")
            else:
                print(f"Studio: {argument.title()} costs {facts['prices'][argument]:,} PKR.")
        else:
            price_answers += 1
            print(f"Studio: Sorry, {argument} is not on our menu.")
    elif command == "/reset":
        messages = [messages[0]]  # forget the chat, keep the rules
        print("Studio: Memory cleared.")
    else:
        messages.append({"role": "user", "content": text})

        # Keep the system message first, then only the newest messages
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        response = precise.invoke(messages)
        messages.append({"role": "assistant", "content": response.text})

        chat_answers += 1
        total_tokens += response.usage_metadata["total_tokens"]
        total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

        print(f"Studio: {response.text}")
        print(f"        (memory: {len(messages)} messages, {response.usage_metadata['input_tokens']} tokens sent)")

print("=" * 50)
print("Session report")
print(
    f"Chat answers: {chat_answers} | Menu descriptions: {menu_descriptions} | "
    f"Posts: {posts} | Price answers: {price_answers}"
)
print(f"AI usage: {total_tokens:,} tokens in {total_seconds:.1f} seconds")
print("=" * 50)