# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-4.1"

tools = [
    {
        "type": "web_search",
    }
]


# First Request
response1 = oci_openai_client.responses.create(
    model=model,
    input="please tell me today break news",
    tools=tools,
    store=False,
    include=["web_search_call.action.sources"],
)
print(response1.output)
