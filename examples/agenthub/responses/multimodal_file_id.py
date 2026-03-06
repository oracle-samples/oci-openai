# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Multi-modality example - file input as uploaded File ID."""

from examples.agenthub.common import client

# Upload a file first
with open("/path/to/file.pdf", "rb") as f:
    file = client.files.create(
        file=f,
        purpose="user_data",
    )

# Use the file in a response
response = client.responses.create(
    model="openai.gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id": file.id,
                },
                {
                    "type": "input_text",
                    "text": "What's discussed in the file?",
                },
            ],
        }
    ],
)
print(response.output_text)
