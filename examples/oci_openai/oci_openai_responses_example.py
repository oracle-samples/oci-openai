# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

# mypy: ignore-errors
from oci_openai import OciOpenAI, OciSessionAuth

COMPARTMENT_ID = "ocid1.tenancy.oc1..dummy"
CONVERSATION_STORE_ID = "ocid1.generativeaiconversationstore.oc1.us-chicago-1.dummy"
OVERRIDE_URL = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
PROFILE_NAME = "oc1"
MODEL = "openai.gpt-4o"
REGION = "us-chicago-1"

PROMPT = "Tell me a three sentence bedtime story about a unicorn."


def get_oci_openai_client():
    return OciOpenAI(
        auth=OciSessionAuth(profile_name=PROFILE_NAME),
        compartment_id=COMPARTMENT_ID,
        region=REGION,
        service_endpoint=OVERRIDE_URL,
        conversation_store_id=CONVERSATION_STORE_ID,
    )


def main():
    client = get_oci_openai_client()
    response = client.responses.create(model=MODEL, input=PROMPT)
    print(response.output[0].content[0].text)


if __name__ == "__main__":
    main()
