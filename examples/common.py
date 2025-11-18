from oci_openai import OciOpenAI, OciSessionAuth

COMPARTMENT_ID = ""
CONVERSATION_STORE_ID = ""
OVERRIDE_URL = ""
PROFILE_NAME = "oc1"
MODEL = "openai.gpt-4o"
REGION = ""
PROMPT = "Tell me a three sentence bedtime story about a unicorn."


oci_openai_client = OciOpenAI(
    auth=OciSessionAuth(profile_name=PROFILE_NAME),
    compartment_id=COMPARTMENT_ID,
    region=REGION,
    service_endpoint=OVERRIDE_URL,
    conversation_store_id=CONVERSATION_STORE_ID,
)
