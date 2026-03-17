# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""
Image Generation tool example.

Image generation tool is only available for customers with access to the OpenAI commercial models.
"""

import base64

from examples.agenthub.common import ppe_client

response = ppe_client.responses.create(
    model="openai.gpt-5.2",
    input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{"type": "image_generation"}],
    store=False,
    stream=False,
)

# Save the generated image to a file
image_data = [
    output.result for output in response.output if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("generated_image.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
    print("Image saved to generated_image.png")
else:
    print("No image was generated.")
    print(response.output_text)
