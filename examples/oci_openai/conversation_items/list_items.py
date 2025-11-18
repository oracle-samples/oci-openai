from rich import print

from examples.common import oci_openai_client

items = oci_openai_client.conversations.items.list(
    "conv_977e8f9d624849a79b8eca5e6d67f69a", limit=10
)
print(items.data)
