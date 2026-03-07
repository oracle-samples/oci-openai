# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""File Search tool example - searches a Vector Store for relevant content."""

from examples.agenthub.common import client

VECTOR_STORE_ID = "<your-vector-store-id>"

response = client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    input="What are shapes of OCI GPU?",
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID],
        }
    ],
)
print(response.output_text)
