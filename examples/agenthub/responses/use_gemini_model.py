# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Examples of using Gemini model."""

from examples.agenthub.common import ppe_client

response = ppe_client.responses.create(
    model="google.gemini-2.5-pro",
    input="What is 2x2?",
)
print(response.output_text)
