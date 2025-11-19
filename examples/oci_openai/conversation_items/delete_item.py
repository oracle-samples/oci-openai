# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

conversation = oci_openai_client.conversations.items.delete(
    conversation_id="conv_977e8f9d624849a79b8eca5e6d67f69a",
    item_id="msg_f7cfcdcf47c944cebb414a495e3c3721",
)
print(conversation)
