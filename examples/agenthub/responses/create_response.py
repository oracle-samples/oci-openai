# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Basic Responses API example using the Agentic API."""

from examples.agenthub.common import client

response = client.responses.create(
    model="openai.gpt-4.1",
    input="What is 2x2?",
)
print(response.output_text)
