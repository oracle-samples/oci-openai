# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import httpx
from openai import OpenAI

from oci_openai import OciSessionAuth

PROJECT_ID = ""  # your Generative AI Project OCID
PROFILE_NAME = "DEFAULT"
REGION = "us-chicago-1"


client = OpenAI(
    base_url=f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    project=PROJECT_ID,
    http_client=httpx.Client(auth=OciSessionAuth(profile_name=PROFILE_NAME)),
)
