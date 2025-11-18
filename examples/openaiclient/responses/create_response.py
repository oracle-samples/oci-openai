from examples.common import oci_openai_client
from rich import print

model = "openai.gpt-5"

# First Request
response1 = oci_openai_client.responses.create(
  model=model,
  input="Explain what OKRs are in 2 sentences.",
  previous_response_id=None, # root of the history
)
print(response1)