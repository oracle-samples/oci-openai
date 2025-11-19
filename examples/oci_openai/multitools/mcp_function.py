# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-4.1"


tools = [
    {
        "type": "mcp",
        "server_label": "deepwiki",
        "require_approval": "never",
        "server_url": "https://mcp.deepwiki.com/mcp",
    },
    {
        "type": "function",
        "name": "get_weather",
        "description": "function to get_weather",
        "parameters": {
            "type": "object",
            "properties": {
                "repoName": {"type": "string", "description": "city or country (e.g. seattle"}
            },
            "required": ["repoName"],
            "additionalProperties": False,
        },
    },
]

messages = [
    {
        "role": "user",
        "content": "please tell me something about facebook/react and get weather for seattle",
    }
]


# parrel_call
response = oci_openai_client.responses.create(model=model, input=messages, tools=tools)
print(response.output)
