# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Examples of using GPT-OSS model hosted by OCI."""

from examples.agenthub.common import client

response = client.responses.create(
    model="openai.gpt-oss-120b",
    input="What is 2x2?",
)
print(response.output_text)
