"""Task 2.4 stretch: Bot Battle, fixed rules versus the AI.

Runs test questions for a small business through simple if/elif keyword rules
(Lesson 1.8 style) and through a local Ollama model. Prints both answers and
counts how many questions the rules could not answer.
"""

from langchain.chat_models import init_chat_model

SYSTEM = (
    "You are the assistant of Sweet Crumbs bakery in Lahore. "
    "Open 9 AM to 9 PM every day. Cupcake 250 PKR, brownie 300 PKR, cake 1800 PKR. "
    "Delivery is free above 2000 PKR inside Lahore. Only use these facts, "
    "and say you do not know if the answer is not here. Answer in 2 short lines."
)

llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.2)

questions = [
    "What are your opening hours?",
    "I want a refund for my cake.",
    "How much is a cupcake?",
    "Can I order a birthday cake for 20 people?",
    "Do you have gluten-free options?",
    "Do you deliver to Gulberg?",
]

rules_failed = 0

for question in questions:
    q = question.lower()

    # Replace these rules with the ones from your own Lesson 1.8 bot.
    if "hours" in q or "open" in q:
        rule_answer = "We are open 9 AM to 9 PM, every day."
    elif "refund" in q:
        rule_answer = "A manager will call you within 1 hour."
    elif "cupcake" in q:
        rule_answer = "A cupcake costs 250 PKR."
    else:
        rule_answer = None

    response = llm.invoke([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ])

    print(f"Question: {question}")
    if rule_answer is None:
        rules_failed += 1
        print("  Rules: (no answer)")
    else:
        print(f"  Rules: {rule_answer}")
    print(f"  AI:    {response.text.strip()}")
    print()

print(f"Rules could not answer {rules_failed} of {len(questions)} questions.")