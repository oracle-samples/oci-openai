# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Streaming Responses API example - prints all streamed events."""

from examples.agenthub.common import oci_openai_client

response_stream = oci_openai_client.responses.create(
    model="openai.gpt-4.1",
    input="What are the shapes of OCI GPUs?",
    stream=True,
)

for event in response_stream:
    print(event)
