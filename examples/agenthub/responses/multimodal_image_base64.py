# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Multi-modality example - image input as base64-encoded data URL."""

import base64

from examples.agenthub.common import client


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("/path/to/image.png")

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
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high",
                },
            ],
        }
    ],
)
print(response.output_text)
