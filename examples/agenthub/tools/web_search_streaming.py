# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Web Search tool example."""

from examples.agenthub.common import client

response_stream = client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    tools=[{"type": "web_search"}],
    input="What was a positive news story on 2026-03-06?",
    stream=True,
)

for event in response_stream:
    print(event)