# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from oci_openai import OciOpenAI, OciSessionAuth

client = OciOpenAI(
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    auth=OciSessionAuth(profile_name="<profile name>"),
    compartment_id="<compartment ocid>",
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
streaming = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
    stream=True
)
for chunk in streaming:
    print(chunk)

