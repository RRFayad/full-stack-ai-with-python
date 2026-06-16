import json
import requests
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
from constants import SYSTEM_PROMPT
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()


class Output(BaseModel):
    step: str
    content: Optional[str]
    tool: Optional[str]
    input: Optional[str]


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.ok:
        return response.content.decode("utf-8")
    return None


available_tools = {"get_weather": get_weather}


message_history = []


def main():
    user_query = input("> ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.responses.parse(
            model="gpt-5.5",
            instructions=SYSTEM_PROMPT,
            input=message_history,
            text_format=Output,
        )

        raw_result = response.output_text
        message_history.append({"role": "assistant", "content": raw_result})

        parsed_result = response.output_parsed

        if parsed_result is None:
            return

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🛠️: {tool_to_call}({tool_input}")

            if tool_to_call is None:
                return
            tool_response = available_tools[tool_to_call](tool_input or "")
            print(f"🛠️: {tool_response}")
            message_history.append(
                {
                    "role": "developer",
                    "content": json.dumps(
                        {
                            "step": "OBSERVE",
                            "tool": tool_to_call,
                            "input": tool_input,
                            "output": tool_response,
                        }
                    ),
                }
            )
            continue

        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break


main()
