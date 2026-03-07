# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Examples of using a GPT-OSS model hosted on a Dedicated AI Cluster on OCI."""

from examples.agenthub.common import client

response = client.responses.create(
    model="<your-dac-endpoint-ocid-that-hosts-the-gpt-oss-model>",
    input="What is 2x2?",
)
print(response.output_text)