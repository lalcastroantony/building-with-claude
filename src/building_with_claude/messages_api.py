from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
from anthropic import Anthropic
from anthropic.types import Message

client = Anthropic()
model = "claude-sonnet-4-5"


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


# temperature was removed and effort is the new way. But it was using lot of tokens and some failures happened. so It is not used now.
def chat(
    messages, system=None, effort="high", max_tokens=1000, stop_sequences=[], tools=None
):
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "stop_sequences": stop_sequences,
    }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system
    message = client.messages.create(**params)

    return message


def stream(messages):
    with client.messages.stream(
        model=model, max_tokens=1000, messages=messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    # final_message = stream.get_final_message() # for DB storage
    # print(f"finale message is {final_message}")


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])
