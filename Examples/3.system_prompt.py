import building_with_claude.messages_api as API

messages = []

API.add_user_message(messages, "How do I solve 5x + 2 = 3 for x?")

# Without system prompt
answer = API.chat(messages)

print(answer)

# With system prompt
system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
finalanswer = API.chat(messages, system=system)

print(finalanswer)
