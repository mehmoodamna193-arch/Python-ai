"""Task 2.3: Persona Bot with Real Facts.

A chat bot with memory for a small business. The business facts live in a
dictionary and are put into the system message, so the AI only uses real
information. The owner can switch the bot's personality with /persona and
look up prices with /price, which never calls the AI. Stretch: /add adds a
new menu item and rebuilds the system message so the AI knows it at once.
"""

from langchain.chat_models import init_chat_model

# Why a config dictionary: the model name, temperature and memory size sit in
# one place, so changing them never means hunting through the code.
config = {"model": "llama3.2", "temperature": 0.2, "max_messages": 8}

# Why facts in a dictionary: the owner fears invented prices, so every fact the
# AI may use lives here. Replace these with your own Module 1 business.
facts = {
    "name": "Sweet Crumbs",
    "type": "bakery",
    "city": "Lahore",
    "hours": "9 AM to 9 PM, every day",
    "delivery": "free above 2000 PKR inside Lahore",
    "phone": "0300-1234567",
    "prices": {"cupcake": 250, "brownie": 300, "cake": 1800, "cookie": 100},
}

personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, no slang",
    "sales": "excited, always suggests one extra item to buy",
}


def build_system(style):
    """Build the system message from facts, so /persona and /add share it."""
    return (
        f"You are the assistant of {facts['name']}, a {facts['type']} in {facts['city']}. "
        f"Opening hours: {facts['hours']}. Delivery: {facts['delivery']}. "
        f"Prices in PKR: {facts['prices']}. "
        f"Only use these facts. If the answer is not in these facts, say you do not know "
        f"and suggest calling {facts['phone']}. Never invent prices or products. "
        f"Your style: {style}. Answer in 2 short lines."
    )


llm = init_chat_model(
    config["model"], model_provider="ollama", temperature=config["temperature"]
)

style = personas["friendly"]
messages = [{"role": "system", "content": build_system(style)}]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, /add <item> <price>, bye")

while True:
    text = input("You: ").strip()
    command = text.lower().split(" ")[0]  # first word, e.g. "/price"
    argument = text[len(command):].strip().lower()  # everything after it

    if text.lower() == "bye":
        print("Bot: Goodbye!")
        break
    elif command == "/persona":
        # Why .get() with a default: a wrong name like "pirate" would crash
        # with a KeyError using personas[name]; .get() falls back to friendly.
        style = personas.get(argument, personas["friendly"])
        messages[0]["content"] = build_system(style)  # rules change, memory stays
        print(f"Bot: Style changed to: {style}")
    elif command == "/price":
        # Why no AI here: a dictionary lookup is free, instant and always
        # correct, so prices can never be invented.
        if argument == "":
            print("Bot: Please type an item, for example /price cupcake")
        elif argument in facts["prices"]:
            print(f"Bot: {argument.capitalize()} costs {facts['prices'][argument]} PKR.")
        else:
            print(f"Bot: Sorry, {argument} is not on our menu.")
    elif command == "/add":
        # Item can have several words, so split off only the last word (price)
        pieces = argument.rsplit(" ", 1)
        if len(pieces) == 2 and pieces[1].isdigit():
            facts["prices"][pieces[0]] = int(pieces[1])
            # Why rebuild messages[0]: the AI only knows what is in the system
            # message, so a new item must be written into it immediately.
            messages[0]["content"] = build_system(style)
            print(f"Bot: Added {pieces[0]} at {pieces[1]} PKR.")
        else:
            print("Bot: Use it like this: /add donut 150")
    elif text == "":
        print("Bot: Please type a question.")
    else:
        messages.append({"role": "user", "content": text})

        # Keep the system message first, then only the newest messages
        messages = [messages[0]] + messages[1:][-config["max_messages"]:]

        response = llm.invoke(messages)
        messages.append({"role": "assistant", "content": response.text})
        print(f"Bot: {response.text}")