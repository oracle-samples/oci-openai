# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Delete a response by ID."""

from examples.agenthub.common import client

# Create a response first
response = client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    input="What is 2x2?",
)
print("Created response ID:", response.id)

# Delete the response by ID
client.responses.delete(response_id=response.id)
print("Deleted response:", response.id)
