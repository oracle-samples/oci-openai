# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import logging

from oci_openai import OciOpenAI, OciSessionAuth

logging.basicConfig(level=logging.DEBUG)


def main():
    client = OciOpenAI(
        # region="us-chicago-1",
        service_endpoint="https://ppe.inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        auth=OciSessionAuth(profile_name="oc1"),
        compartment_id="ocid1.tenancy.oc1..aaaaaaaaumuuscymm6yb3wsbaicfx3mjhesghplvrvamvbypyehh5pgaasna",
    )
    model = "meta.llama-4-scout-17b-16e-instruct"

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.model_dump_json())

    # Process the stream
    print("=" * 80)
    print("Process in streaming mode")
    streaming = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
        stream=True,
    )
    for chunk in streaming:
        print(chunk)


if __name__ == "__main__":
    main()
