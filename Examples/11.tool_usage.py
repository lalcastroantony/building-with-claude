from anthropic import Anthropic
from dotenv import load_dotenv

import building_with_claude.tool as ToolUse

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

messages = []

messages.append(
    {"role": "user", "content": "What is the exact time, formatted as HH:MM:SS?"}
)

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[ToolUse.get_current_datetime_schema],
)

# print(response.content[0].input)

messages.append({"role": "assistant", "content": response.content})

current_datetime = ToolUse.get_current_datetime(**response.content[0].input)

messages.append(
    {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": response.content[0].id,
                "content": current_datetime,
                "is_error": False,
            }
        ],
    }
)

final_response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[ToolUse.get_current_datetime_schema],
)

print(final_response.content[0].text)
