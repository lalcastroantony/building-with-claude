import building_with_claude.messages_api as API

messages = []

API.add_user_message(messages, "CBSE vs EdExcel IGCSE")

API.stream(messages)
