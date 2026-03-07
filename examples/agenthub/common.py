# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import os
from openai import OpenAI

REGION = "us-chicago-1"

client = OpenAI(
    base_url=f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/openai/v1",
    api_key=os.getenv("OCI_GENAI_API_KEY"),
    project=os.getenv("OCI_GENAI_PROJECT_ID"),
)
