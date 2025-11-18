from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-5"

# Streaming request
stream = oci_openai_client.responses.create(
    model=model,
    input="Explain what OKRs are in 2 sentences.",
    previous_response_id=None,
    stream=True,
)

# Process the stream
print("Streaming response:")
for chunk in stream:
    print(chunk)

print("\n")  # New line after streaming completes
