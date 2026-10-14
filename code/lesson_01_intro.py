name = "Amna"
goal = "AI Agent Developer"
print(f"Hi, I am {name} and I will become an {goal}.")
"""Lesson 1.4: Build a prompt from user input."""

# Collect details from the user
role = input("AI role (e.g. engineer): ")
topic = input("Topic: ")
level = input("Level (beginner/expert): ")

# Build the final prompt (this is what we will send to an LLM later)
prompt = f"You are a {role}. Explain {topic} to a {level} in 3 bullet points."

print("\n--- Your Prompt ---")
print(prompt)