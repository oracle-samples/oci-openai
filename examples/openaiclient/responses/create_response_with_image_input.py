import base64
from examples.common import oci_openai_client
from rich import print

model = "openai.gpt-5"

# Read and encode image
with open("openaiclient/responses/Cat.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

response1 = oci_openai_client.responses.create(
    model=model,
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what's in this image?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_data}",
                },
            ],
        }
    ],
)

print(response1.output)