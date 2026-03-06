# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from oci_openai import OciOpenAI, OciSessionAuth

PROJECT_ID = ""  # your Generative AI Project OCID
PROFILE_NAME = "DEFAULT"
REGION = "us-chicago-1"


oci_openai_client = OciOpenAI(
    auth=OciSessionAuth(profile_name=PROFILE_NAME),
    project=PROJECT_ID,
    region=REGION,
)
