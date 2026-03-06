# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Examples of using different model providers through the Agentic API."""

from examples.agenthub.common import oci_openai_client

# 3rd-party model provider (e.g., xAI Grok)
response = oci_openai_client.responses.create(
    model="xai.grok-4",
    input="What are the shapes of OCI GPUs?",
)
print("Grok response:", response.output_text)

# OCI-hosted model using shared serving infrastructure (On-Demand mode)
response = oci_openai_client.responses.create(
    model="openai.gpt-oss-120b",
    input="What are the shapes of OCI GPUs?",
)
print("GPT-OSS response:", response.output_text)

# OCI-hosted model using your own Dedicated AI Cluster
# response = oci_openai_client.responses.create(
#     model="<your-dac-endpoint-ocid>",
#     input="What are the shapes of OCI GPUs?",
# )
# print("DAC response:", response.output_text)
