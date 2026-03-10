# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Create a response without storing it."""

from examples.agenthub.common import client

response = client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    input="What is 2x2?",
    store=False,
)
print(response.output_text)

# Try to retrieve the response by ID, and it should throw openai.NotFoundError
retrieved = client.responses.retrieve(response_id=response.id)
