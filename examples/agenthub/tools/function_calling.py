# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Function Calling (local function tool) example."""

import json

from openai.types.responses import ResponseFunctionToolCall
from openai.types.responses.response_input_param import FunctionCallOutput

from examples.agenthub.common import client

model = "xai.grok-4-1-fast-reasoning"


# Define local functions
def get_current_weather(location: str) -> dict:
    """Mock weather function."""
    return {
        "location": location,
        "temperature": "72",
        "unit": "fahrenheit",
        "forecast": ["sunny", "windy"],
    }


# Define function tool schema
function_tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "Get current weather for a given location.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogota, Colombia",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
    }
]

# First API request - model decides to call the function
response = client.responses.create(
    model=model,
    input="What is the weather in Seattle?",
    tools=function_tools,
)
print("First response:", response.output)

# If the model requested a function call, execute it and send the result back
if isinstance(response.output[0], ResponseFunctionToolCall):
    tool_call = response.output[0]
    function_args = json.loads(tool_call.arguments)

    # Execute the local function
    result = get_current_weather(**function_args)

    # Second API request - send the function output back to the model
    response = client.responses.create(
        model=model,
        input=[
            FunctionCallOutput(
                type="function_call_output",
                call_id=tool_call.call_id,
                output=json.dumps(result),
            )
        ],
        previous_response_id=response.id,
        tools=function_tools,
    )
    print("Final response:", response.output_text)
