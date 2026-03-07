# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Long-Term Memory example - durable memory across conversations using memory_subject_id."""

import time

from examples.agenthub.common import client

model = "xai.grok-4-1-fast-reasoning"

# First conversation - store preferences
conversation1 = client.conversations.create(
    metadata={"memory_subject_id": "user_123456"},
)

response = client.responses.create(
    model=model,
    input="I like Fish. I don't like Shrimp.",
    conversation=conversation1.id,
)
print("Response 1:", response.output_text)

# Delay for long-term memory processing
print("Waiting for long-term memory processing...")
time.sleep(10)

# Second conversation - recall preferences
conversation2 = client.conversations.create(
    metadata={"memory_subject_id": "user_123456"},
)

response = client.responses.create(
    model=model,
    input="What do I like?",
    conversation=conversation2.id,
)
print("Response 2:", response.output_text)
