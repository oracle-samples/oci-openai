# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Long-Term Memory with access policy control.

memory_access_policy options:
  - recall_and_store: enable both store and recall (default)
  - recall_only: can recall memory but cannot store new memory
  - store_only: can store memory but cannot recall memory
  - none: neither store nor recall
"""

import time

from examples.agenthub.common import client

model = "openai.gpt-4.1"

# First conversation - store only (no recall)
conversation1 = client.conversations.create(
    metadata={
        "memory_subject_id": "user_123456",
        "memory_access_policy": "store_only",
    },
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

# Second conversation - recall only (no new storage)
conversation2 = client.conversations.create(
    metadata={
        "memory_subject_id": "user_123456",
        "memory_access_policy": "recall_only",
    },
)

response = client.responses.create(
    model=model,
    input="What do I like?",
    conversation=conversation2.id,
)
print("Response 2:", response.output_text)
