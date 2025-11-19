# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import base64

from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-5"

# Read and encode image
with open("openaiclient/responses/Cat.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

response1 = oci_openai_client.responses.create(
    model=model,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "what's in this image?"},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_data}",
                },
            ],
        }
    ],
)

print(response1.output)
