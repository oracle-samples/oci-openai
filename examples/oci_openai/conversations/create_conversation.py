from rich import print

from examples.common import oci_openai_client

conversation = oci_openai_client.conversations.create(
    metadata={"topic": "demo"}, items=[{"type": "message", "role": "user", "content": "Hello!"}]
)
print(conversation)
