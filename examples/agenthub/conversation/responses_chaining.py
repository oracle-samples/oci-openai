# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Multi-turn conversation using Responses Chaining (previous_response_id)."""

from examples.agenthub.common import oci_openai_client

model = "openai.gpt-4.1"

# First turn
response1 = oci_openai_client.responses.create(
    model=model,
    input="Tell me a joke. Keep it short.",
)
print("Response 1:", response1.output_text)

# Second turn, chaining to the first
response2 = oci_openai_client.responses.create(
    model=model,
    input="Why is it funny?",
    previous_response_id=response1.id,
)
print("Response 2:", response2.output_text)
