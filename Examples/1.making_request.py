import building_with_claude.messages_api as API

messages = []
API.add_user_message(messages, "What is quantum computing? Answer in one sentence")

answer = API.chat(messages)

print(answer)
