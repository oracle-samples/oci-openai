# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

items = oci_openai_client.conversations.items.create(
    "conv_977e8f9d624849a79b8eca5e6d67f69a",
    items=[
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "Hello!"}],
        },
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "How are you?"}],
        },
    ],
)
print(items.data)
