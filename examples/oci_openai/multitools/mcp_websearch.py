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
        "type": "web_search",
    },
]


# parrel_call
response = oci_openai_client.responses.create(
    model=model,
    input="search latest repo related to react, and use deepwiki tell me repo structure",
    tools=tools,
)
print(response.output)
