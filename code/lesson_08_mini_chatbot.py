"""Task 1.8: City Care Clinic chatbot.

A rule-based chatbot for a local clinic. It answers the common questions
(timings, fees, location, appointments), hands complaints and requests for a
human to staff, and counts the questions it could not answer. For those it
prints the AI prompt we would send in Module 2. The design (intents,
keywords, replies) is in README.md. Type 'bye' to exit.
"""

BOT = "City Care Bot"
CLINIC = "City Care Clinic"

print(f"{BOT}: Hi! Ask about timings, fees, location or appointments. Type 'bye' to exit.")

# Why: the name is asked once, before the loop, so every reply can use it
# without asking again on every message.
name = input(f"{BOT}: What is your name? ").strip().title()

message_count = 0
unanswered_count = 0
complaint_count = 0

while True:
    # Why: strip() + lower() make "  BYE " and "bye" identical, so the bot
    # doesn't miss keywords because of random capitals or spaces.
    message = input(f"{name}: ").strip().lower()

    # Why: an empty message is not a real question, so it is skipped instead
    # of being counted as "unanswered" and sent to the AI with no text.
    if not message:
        print(f"{BOT}: Please type your question.")
        continue

    message_count += 1

    # Why: punctuation removed and the message split into words, so short
    # keywords like "hi" or "late" only match whole words, never the middle
    # of another word like "history" or "chocolate".
    words = message.replace("?", " ").replace("!", " ").replace(",", " ").replace(".", " ").split()

    if message == "bye":
        print(f"{BOT}: Take care, {name}!")
        break

    # Why: complaints and human requests are checked FIRST, so an unhappy
    # customer is never given a cheerful canned answer by mistake.
    elif any(w in words for w in ("agent", "human")):
        print(f"{BOT}: Connecting you to a human...")
        break
    elif any(w in words for w in ("late", "complaint", "rude", "bad", "wrong", "refund", "problem")):
        complaint_count += 1
        print(f"{BOT}: Sorry about that, {name}. The clinic manager will call you today.")
    elif words and words[0] in ("hi", "hello", "salam", "hey"):
        print(f"{BOT}: Hello, {name}! How can I help you?")
    elif any(w in words for w in ("timing", "timings", "time", "open", "close", "hours")):
        print(f"{BOT}: We are open 10 am to 8 pm, Monday to Saturday.")
    elif any(w in words for w in ("fee", "fees", "price", "cost", "charges")):
        print(f"{BOT}: Consultation fee is 2,000 PKR.")
    elif any(w in words for w in ("where", "location", "address", "directions")):
        print(f"{BOT}: We are at 12 Garden Road, near the main market.")
    elif any(w in words for w in ("appointment", "book", "booking", "schedule")):
        print(f"{BOT}: Call 0300-1234567 or reply with your preferred day and time to book.")
    else:
        # Why: unanswered questions are counted so the owner can see which
        # questions still need help, and the prompt is what Module 2's AI will get.
        unanswered_count += 1
        prompt = (
            f"You are the friendly assistant of {CLINIC}. "
            f"Answer in 2 lines: {message}"
        )
        print(f"{BOT}: I am not sure yet. In Module 2, an AI will answer: {prompt}")

print("=" * 40)
print(f"Chat summary: {message_count} messages, {unanswered_count} unanswered, "
      f"{complaint_count} complaints.")
      