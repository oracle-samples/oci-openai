# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Code Interpreter tool example - writes and runs code in a sandbox."""

from examples.agenthub.common import ppe_client

response = ppe_client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    tools=[
        {
            "type": "code_interpreter",
            "container": {"type": "auto", "memory_limit": "4g"},
        }
    ],
    instructions="Write and run code using the python tool to answer the question.",
    input="I need to solve the equation 3x + 11 = 14. Can you help me?",
)
print(response)
