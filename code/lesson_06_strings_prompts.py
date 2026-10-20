"""Task 1.6: Clean, measure and safely size a customer question.

Asks for a name and a messy question, cleans both, prints the character
count and estimated tokens, checks whether the question mentions "python",
then builds a multi-line prompt that is safe to send to an AI.
Stretch: masks a bad word and prints an example cost using :.2f.
"""

raw_name = input("Your name: ")
raw_question = input("Your question: ")

# Why: strip() removes stray spaces and title()/capitalize() fix random
# capitals, so the AI always receives the same tidy text.
name = raw_name.strip().title()
question = raw_question.strip().capitalize()

# Stretch - Why: masking rude words before the prompt is built keeps them
# from ever reaching the AI (or the logs).
question = question.replace("stupid", "***")

characters = len(question)
# Why: about 4 characters make 1 token in English, so this is a quick
# estimate of size and cost without needing a real tokenizer.
estimated_tokens = round(characters / 4)

# Why: lower() makes the check ignore capitals, so "PYTHON" and "Python" both match.
mentions_python = "python" in question.lower()

# Stretch: example price only (0.5 PKR per 1K tokens), not a real quote.
estimated_cost = estimated_tokens / 1000 * 0.5

print("=" * 40)
print(f"Cleaned question: {question}")
print(f"Characters: {characters}, about {estimated_tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print(f"Estimated cost (example price): {estimated_cost:.2f} PKR")
print("=" * 40)

# Why: slicing [:150] caps the question length, so a huge pasted text can't
# make the prompt (and the bill) too large.
prompt = f"""You are a friendly Python tutor.
Greet {name} by name and answer in 3 short lines.
Question: {question[:150]}"""

print(prompt)