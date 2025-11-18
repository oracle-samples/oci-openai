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
