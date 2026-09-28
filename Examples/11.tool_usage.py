import json

from anthropic import Anthropic
from dotenv import load_dotenv

import building_with_claude.messages_api as MessageAPI
import building_with_claude.tool as ToolUse

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

messages = []

MessageAPI.add_user_message(
    messages,
    "Set a reminder for my doctors appointment. Its 177 days after Jan 1st, 2050.",
)


def run_conversation(messages):
    while True:
        response = MessageAPI.chat(
            messages,
            tools=[
                ToolUse.get_current_datetime_schema,
                ToolUse.add_duration_to_datetime_schema,
                ToolUse.set_reminder_schema,
            ],
        )
        MessageAPI.add_assistant_message(messages, response)
        print(MessageAPI.text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        MessageAPI.add_user_message(messages, tool_results)

    return messages


def run_tools(message):
    tool_requests = [block for block in message.content if block.type == "tool_use"]
    tool_result_blocks = []
    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False,
            }
        except Exception as e:  # noqa: BLE001
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True,
            }
        tool_result_blocks.append(tool_result_block)
    return tool_result_blocks


def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return ToolUse.get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return ToolUse.add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return ToolUse.set_reminder(**tool_input)


run_conversation(messages)
