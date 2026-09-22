import building_with_claude.messages_api as API

messages = []

API.add_user_message(
    messages, "What do you think about CBSE vs International schools in India?"
)

# Low effort - less reasoning, fewer tokens, faster
print(API.chat(messages, effort="low"))

# High effort - more reasoning, more tokens
print(API.chat(messages, effort="high", max_tokens=16000))
