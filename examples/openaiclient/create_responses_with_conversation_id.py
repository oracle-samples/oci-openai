from examples.common import oci_openai_client
from rich import print

model = "openai.gpt-4.1"

conversation = oci_openai_client.conversations.create(
  metadata={"topic": "demo"}
)
print(conversation)

response = oci_openai_client.responses.create(
  model=model,
  input="Explain what OKRs are in 2 sentences.",
  conversation=conversation.id
)
print(response.output)

response = oci_openai_client.responses.create(
  model=model,
  input="what was my previous question from user?",
  conversation=conversation.id
)
print(response.output)

response = oci_openai_client.responses.create(
  model=model,
  input="Based on that, list 3 common pitfalls to avoid.",
  conversation=conversation.id
)
print(response.output)