import building_with_claude.messages_api as API

messages = []

API.add_user_message(
    messages, "Write a Python function that checks whether a string is a palindrome."
)
API.add_assistant_message(messages, "```python")

code = API.chat(messages, stop_sequences=["```"])

print(code.strip())
