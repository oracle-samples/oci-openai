# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Short-Term Memory Optimization (STMO) example.

STMO auto-condenses chat history with key information to reduce token usage and latency.
Enable STMO in the project settings, or per-conversation via metadata flag.
"""

from examples.agenthub.common import client

model = "openai.gpt-4.1"

# Create a conversation with STMO enabled
conversation = client.conversations.create(
    metadata={"topic": "demo", "short_term_memory_optimization": "True"},
    items=[{"type": "message", "role": "user", "content": "Hello!"}],
)

# Multiple turns - STMO will auto-condense the history
response = client.responses.create(
    model=model,
    input="I like Fish.",
    conversation=conversation.id,
)
print("Turn 1:", response.output_text)

response = client.responses.create(
    model=model,
    input="I like Beef.",
    conversation=conversation.id,
)
print("Turn 2:", response.output_text)

response = client.responses.create(
    model=model,
    input="I like ice-cream.",
    conversation=conversation.id,
)
print("Turn 3:", response.output_text)

response = client.responses.create(
    model=model,
    input="I like coffee.",
    conversation=conversation.id,
)
print("Turn 4:", response.output_text)

# The STMO summary will be generated automatically
