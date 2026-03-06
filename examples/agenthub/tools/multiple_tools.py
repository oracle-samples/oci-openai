# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Using multiple tools in a single request."""

from examples.agenthub.common import client

response_stream = client.responses.create(
    model="openai.gpt-4.1",
    tools=[
        {"type": "web_search"},
        {
            "type": "mcp",
            "server_label": "gitmcp",
            "server_url": "https://gitmcp.io/openai/tiktoken",
            "allowed_tools": [
                "search_tiktoken_documentation",
                "fetch_tiktoken_documentation",
            ],
            "require_approval": "never",
        },
        {
            "type": "mcp",
            "server_label": "dmcp",
            "server_description": "A Dungeons and Dragons MCP server to assist with dice rolling.",
            "server_url": "https://mcp.deepwiki.com/mcp",
            "require_approval": "never",
        },
    ],
    input="What are top news in Seattle today? How does tiktoken work? Roll 2d4+1.",
    stream=True,
)

for event in response_stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)

print()
