"""Task 2.1: AI Tutor.

Asks the student for a topic and a level, sends them to a local Ollama
model through LangChain, then prints the answer together with the total
tokens used and the time taken in seconds.
"""

from langchain.chat_models import init_chat_model

# Why low temperature: a tutor should give focused, repeatable explanations,
# not creative or random ones.
llm = init_chat_model("gemma3:1b", model_provider="ollama", temperature=0.2)

# Why .strip(): users often add accidental spaces, and we want clean values
# inside the system message.
topic = input("Topic:   ").strip()
level = input("Level (beginner or expert): ").strip()

# Why a system message: it sets the AI's role, the student's level and the
# answer length once, so the user message can stay as just the topic.
system_message = (
    f"You are a friendly tutor at a tuition centre. "
    f"Explain the topic for a {level} student. "
    f"Answer in 3 short lines."
)

response = llm.invoke([
    {"role": "system", "content": system_message},
    {"role": "user", "content": topic},
])

# total_duration is in nanoseconds, so divide to get seconds
seconds = response.response_metadata["total_duration"] / 1_000_000_000
total_tokens = response.usage_metadata["total_tokens"]

print("=" * 40)
print(response.text)
print("=" * 40)
print(f"{total_tokens} tokens in {seconds:.1f} seconds")