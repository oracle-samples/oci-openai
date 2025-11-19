# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-4.1"
tools = [
    {
        "type": "mcp",
        "server_label": "stripe",
        "require_approval": "never",
        "server_url": "https://mcp.stripe.com",
        "authorization": "<test key>",
    },
    {
        "type": "mcp",
        "server_label": "deepwiki",
        "require_approval": "never",
        "server_url": "https://mcp.deepwiki.com/mcp",
    },
]
response1 = oci_openai_client.responses.create(
    model=model,
    input="Please use stirpe create account with a and a@g.com and "
    "use deepwiki understand facebook/react",
    tools=tools,
    store=True,
)

print(response1.output)
