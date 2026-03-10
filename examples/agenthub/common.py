# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import os
from openai import OpenAI
import httpx
from oci_openai import OciSessionAuth

"""
This file contains the common code for the examples in the examples/agenthub directory.
"""


REGION = "us-chicago-1"

# The base url for Responses API, Conversations API, Files API, Vector Stores Files API, Containers API
DATA_PLANE_URL = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com/openai/v1"

# The base url for Vector Stores API
CONTROL_PLANE_URL = f"https://generativeai.{REGION}.oci.oraclecloud.com/20231130/openai/v1"

# Create the client to interact with Responses API, Conversations API, Files API, Containers API
client = OpenAI(
    base_url=DATA_PLANE_URL,
    api_key=os.getenv("OCI_GENAI_API_KEY"),
    project=os.getenv("OCI_GENAI_PROJECT_ID"),
)

# Create the client to interact with Vector Stores API and Vector Store Files API
cp_client = OpenAI(
    base_url=CONTROL_PLANE_URL,
    # Using IAM auth as API key is not yet supported for Vector Stores API
    api_key="not-used",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)


KIX_REGION = "ap-osaka-1"

# Responses API, Conversations API, Files API, Containers API use the data plane base URL
DATA_PLANE_URL = f"https://inference.generativeai.{KIX_REGION}.oci.oraclecloud.com/openai/v1"

# Vector Stores API uses the control plane base URL
CONTROL_PLANE_URL = f"https://generativeai.{KIX_REGION}.oci.oraclecloud.com/20231130/openai/v1"

# Create the client to interact with Responses API, Conversations API, Files API, Containers API
kix_client = OpenAI(
    base_url=DATA_PLANE_URL,
    api_key="not-used",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
    project="ocid1.generativeaiproject.oc1.ap-osaka-1.amaaaaaacqy6p4qa5fsnlo47sdab2eea7bc6ikdfulpziu5z5ox3d5mlzqyq",
)

# Create the client to interact with Vector Stores API and Vector Store Files API
kix_cp_client = OpenAI(
    base_url=CONTROL_PLANE_URL,
    # Using IAM auth as API key is not yet supported for Vector Stores API
    api_key="not-used",
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)