# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Web Search tool example."""

from examples.agenthub.common import client

response = client.responses.create(
    model="openai.gpt-4.1",
    tools=[{"type": "web_search"}],
    input="What was a positive news story on 2025-11-14?",
)
print(response.output_text)
