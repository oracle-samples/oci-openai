# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Multi-modality example - image input as internet-accessible URL."""

from examples.agenthub.common import client

response = client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    store=False,
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "What's in this image?",
                },
                {
                    "type": "input_image",
                    "image_url": "https://picsum.photos/id/237/200/300",
                },
            ],
        }
    ],
)
print(response.output_text)
