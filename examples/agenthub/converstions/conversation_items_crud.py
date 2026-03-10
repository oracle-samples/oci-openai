# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples.agenthub.common import client

# Create an empty conversation
conversation = client.conversations.create()
print("\nCreated conversation:", conversation)


# Create items in the conversation
client.conversations.items.create(
    conversation_id=conversation.id,
    items=[
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "What's your name?"}],
        },
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "What's your favorite color?"}],
        },
    ],
)

# List the items in the conversation after creating items
items = client.conversations.items.list(
    conversation_id=conversation.id,
)
print("\nConversation items after creating items:", items.data)


# Delete an item from the conversation
client.conversations.items.delete(
    conversation_id=conversation.id,
    item_id=items.data[0].id,
)


# List the items in the conversation after deleting an item
items = client.conversations.items.list(
    conversation_id=conversation.id,
)
print("\nConversation items after creating items:", items.data)
