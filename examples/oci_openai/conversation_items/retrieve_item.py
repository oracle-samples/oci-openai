from rich import print

from examples.common import oci_openai_client

item = oci_openai_client.conversations.items.retrieve(
    conversation_id="conv_977e8f9d624849a79b8eca5e6d67f69a",
    item_id="msg_f7cfcdcf47c944cebb414a495e3c3721",
)
print(item)
