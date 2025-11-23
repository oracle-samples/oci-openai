# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import json
from typing import Dict

from examples.common import oci_openai_client

model = "openai.gpt-4.1"


def get_current_weather(location: str, unit: str = "fahrenheit") -> Dict[str, str]:
    # Simple stand-in for a real weather lookup.
    return {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }


messages = [
    {
        "role": "user",
        "content": "What is the weather like in Boston and San Francisco?",
    }
]
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a specific location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, for example Boston, MA.",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit to use in the response.",
                    },
                },
                "required": ["location"],
            },
        },
    }
]

first_response = oci_openai_client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
first_choice = first_response.choices[0]

if first_choice.finish_reason == "tool_calls":
    call_message = first_choice.message
    new_messages = messages + [call_message]
    for tool_call in call_message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        tool_result = get_current_weather(
            location=args.get("location", ""),
            unit=args.get("unit", "fahrenheit"),
        )
        new_messages.append(
            {
                "role": "tool",
                "name": tool_call.function.name,
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result),
            }
        )

    follow_up = oci_openai_client.chat.completions.create(
        model=model,
        messages=new_messages,
    )
    print(follow_up.choices[0].message.content)
else:
    print(first_choice.message.content)
