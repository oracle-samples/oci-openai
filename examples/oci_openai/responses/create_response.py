from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-5"

# First Request
response1 = oci_openai_client.responses.create(
    model=model,
    input="Explain what OKRs are in 2 sentences.",
    previous_response_id=None,  # root of the history
)
print(response1)
