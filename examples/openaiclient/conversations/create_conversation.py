from examples.common import oci_openai_client
from rich import print


conversation = oci_openai_client.conversations.create(
  metadata={"topic": "demo"},
  items=[
    {"type": "message", "role": "user", "content": "Hello!"}
  ]
)
print(conversation)