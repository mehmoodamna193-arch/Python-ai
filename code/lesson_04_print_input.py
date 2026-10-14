name = input("Enter your name: ")
business = input("What type of business do you have (e.g. bakery)? ")
problem = input("What is one problem you face? ")
prompt = f"Suggest 3 AI solutions for a {business} that struggles with {problem}."

print(f"\nWelcome, {name}! Here is your prompt:\n")

print(prompt)
