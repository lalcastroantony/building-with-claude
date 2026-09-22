import json

import building_with_claude.messages_api as API

messages = []

messages = []

API.add_user_message(messages, "Generate a very short event bridge rule as json")
API.add_assistant_message(messages, "```json")

text = API.chat(messages, stop_sequences=["```"])

print(text)

# Clean up and parse the JSON
clean_json = json.loads(text.strip())
