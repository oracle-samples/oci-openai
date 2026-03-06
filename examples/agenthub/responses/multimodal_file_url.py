# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Multi-modality example - file input as internet-accessible URL."""

from examples.agenthub.common import oci_openai_client

response = oci_openai_client.responses.create(
    model="openai.gpt-4.1",
    store=False,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What is in this file?"},
                {
                    "type": "input_file",
                    "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                },
            ],
        }
    ],
)
print(response.output_text)
