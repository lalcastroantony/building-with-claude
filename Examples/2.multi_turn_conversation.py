import building_with_claude.messages_api as API

# Start with an empty message list
messages = []

# Add the initial user question
API.add_user_message(messages, "Define quantum computing in one sentence")

# Get Claude's response
answer = API.chat(messages)

print(answer)

# Add Claude's response to the conversation history
API.add_assistant_message(messages, answer)

# Add a follow-up question
API.add_user_message(messages, "Write another sentence")

# Get the follow-up response with full context
final_answer = API.chat(messages)

print(final_answer)
