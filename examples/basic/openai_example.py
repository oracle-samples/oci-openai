# mypy: ignore-errors
from oci_openai.oci_openai import OciOpenAI, OciSessionAuth

COMPARTMENT_ID = "ocid1.tenancy.oc1..aaaaaaaaumuuscymm6yb3wsbaicfx3mjhesghplvrvamvbypyehh5pgaasna"
CONVERSATION_STORE_ID = "ocid1.generativeaiconversationstore.oc1.us-chicago-1.amaaaaaacqy6p4qa255d2l74gt32zmemfmeywdusxuycpzzur4hvq7k2yt5q"
OVERRIDE_URL="https://ppe.inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1"
PROFILE_NAME = "oc1"
MODEL = "openai.gpt-4o"
REGION = "us-chicago-1"

PROMPT="Tell me a three sentence bedtime story about a unicorn."

def get_oci_openai_client():
    return OciOpenAI(
        auth=OciSessionAuth(profile_name=PROFILE_NAME),
        compartment_id=COMPARTMENT_ID,
        region=REGION,
        override_url=OVERRIDE_URL,
        conversation_store_id=CONVERSATION_STORE_ID,
    )

def main():
    client = get_oci_openai_client()
    # response = client.responses.create(
    #     model=MODEL,
    #     input=PROMPT
    # )
    # print(response.output[0].content[0].text)

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.model_dump_json())

if __name__ == "__main__":
    main()