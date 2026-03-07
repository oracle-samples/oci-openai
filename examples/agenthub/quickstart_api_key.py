# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Quickstart using Generative AI API Key authentication.

This example uses the native OpenAI client with OCI Generative AI API Key.
No oci-openai package needed for API Key auth - just the official OpenAI SDK.

Steps:
  1. Create a Generative AI Project on OCI Console
  2. Create a Generative AI API Key on OCI Console
  3. Run this script
"""

from openai import OpenAI

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # your OCI GenAI API Key
    project="ocid1.generativeaiproject.oc1.us-chicago-1.xxxxxxxx",  # your OCI GenAI Project OCID
)

response = client.responses.create(
    model="xai.grok-4-1-fast-reasoning",
    input="What is 2x2?",
)
print(response.output_text)
