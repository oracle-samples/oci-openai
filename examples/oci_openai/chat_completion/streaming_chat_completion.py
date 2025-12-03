# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples.common import oci_openai_client

model = "openai.gpt-4.1"

stream = oci_openai_client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "You are a concise assistant who answers in one paragraph.",
        },
        {
            "role": "user",
            "content": "Explain why the sky is blue as if you were a physics teacher.",
        },
    ],
    stream=True,
)

for chunk in stream:
    for choice in chunk.choices:
        delta = choice.delta
        if delta.content:
            print(delta.content, end="", flush=True)
print()
