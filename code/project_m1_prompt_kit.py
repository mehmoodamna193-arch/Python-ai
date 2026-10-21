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
 
## LLM prompts in action