# mypy: ignore-errors

# OpenAI Agents SDK imports
from agents import Agent, Runner, set_default_openai_client, trace
import asyncio

# OCI OpenAI Client SDK imports
from oci_openai.oci_openai import AsyncOciOpenAI, OciSessionAuth

# set_default_openai_key(openai_apikey)
COMPARTMENT_ID = ""
CONVERSATION_STORE_ID = ""
OVERRIDE_URL=""
REGION = ""
PROFILE_NAME = "oc1"
MODEL = "openai.gpt-4o"


# Create OCI OpenAI Client passing auth and runtime configuration
def get_oci_openai_client():
    return AsyncOciOpenAI(
        auth=OciSessionAuth(profile_name=PROFILE_NAME),
        compartment_id=COMPARTMENT_ID,
        region=REGION,
        override_url=OVERRIDE_URL,
        conversation_store_id=CONVERSATION_STORE_ID,
    )

# Set the OCI OpenAI Client as the default client to use with OpenAI Agents
set_default_openai_client(get_oci_openai_client())

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=MODEL
    )
    with trace("Trace workflow"):
        result = await Runner.run(agent, "Write a haiku about recursion in programming.")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
