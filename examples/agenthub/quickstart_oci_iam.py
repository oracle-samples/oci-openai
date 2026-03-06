# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Quickstart using OCI IAM authentication.

This example uses the oci-openai package for OCI IAM auth.

Steps:
  1. Create a Generative AI Project on OCI Console
  2. pip install oci-openai
  3. Run this script
"""

import httpx
from openai import OpenAI

from oci_openai import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    project="ocid1.generativeaiproject.oc1.us-chicago-1.xxxxxxxx",  # your Project OCID
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)

response = client.responses.create(
    model="openai.gpt-4.1",
    input="What is 2x2?",
)
print(response.output_text)
