"""Module 1 project: AI Prompt Kit (upgraded in Lesson 2.1).

Asks for business details, builds three prompts, prints them, and now sends
Prompt 1 (marketing) straight to a local Ollama model through LangChain,
so you no longer copy-paste it. Prints the answer, tokens and time.
"""

from langchain.chat_models import init_chat_model

LINE = "=" * 60
business_name = input("Business name: ")
business_type = input("Business type (e.g. bakery): ")
city = input("City: ")
customers = input("Main customers (e.g. students, families): ")

budget = int(input("Monthly budget in PKR: ")) #explicite conversion from string to integer
marketing_prompt = (
    f"post idea for {business_name}, a {business_type} in {city}. "
    f"a short caption and 3 relevant hashtags. Keep the tone friendly."
)
service_prompt = (
    f"{business_name} in {city}. Write a polite, empathetic reply to an "
    f"unhappy customer who had a bad experience. Apologise sincerely, offer to make it right, and keep "
    f"it under 100 words."
) 
#formatting string
#triple quotes are used for multi-line strings 
#same as lesson 07 
 
growth_prompt = (
    f"You are a business growth advisor. Suggest 3 low-cost ways AI can "
    f"help {business_name}, a {business_type} in {city} serving "
    f"{customers}, grow its business. Our total monthly budget is "
    f"PKR {budget:,}. For each idea, give the estimated monthly cost in "
    f"PKR and the first step to start."
)

print(f"\n{LINE}")
print(f"  AI PROMPTS FOR {business_name.upper()}")
print(LINE)
 
print("\nPROMPT 1 - MARKETING")
print("-" * 60)
print(marketing_prompt)
 
print("\nPROMPT 2 - CUSTOMER SERVICE")
print("-" * 60)
print(service_prompt)
 
print("\nPROMPT 3 - GROWTH")
print("-" * 60)
print(growth_prompt)

# LLM prompts in action
# Why create the model after the prompts are printed: if Ollama is not
# running, you still see all three prompts before any connection error.
# Why temperature 0.7: captions and hashtags are creative work, so we want
# some variety, but not the wildness of 1.0+.
llm = init_chat_model("llama3.2", model_provider="ollama", temperature=0.7)

print("\nAI ANSWER TO PROMPT 1 - MARKETING")
print("-" * 60)
print("Thinking... (the first call is slow while the model loads)")

response = llm.invoke([{"role": "user", "content": marketing_prompt}])

# total_duration is in nanoseconds, so divide to get seconds
seconds = response.response_metadata["total_duration"] / 1_000_000_000
total_tokens = response.usage_metadata["total_tokens"]

print(response.text)
print(LINE)
print(f"{total_tokens} tokens in {seconds:.1f} seconds")
