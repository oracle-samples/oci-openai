from examples.common import oci_openai_client
from rich import print

  #  "authorization": "12_sk_test_51SFhniEEmUnXltbbsCMqcyZ4LhCvrYM9euoqZ47vAYurryCe84s9LmgJ3f21yFXefqkBOTaAq7Yf3WFa9Vlmcr4r00GjZUQfru",
   

model = "openai.gpt-4.1"
tools = [
    {
        "type": "mcp",
        "server_label": "stripe",
       "require_approval": "never",
       "server_url": "https://mcp.stripe.com",
       "authorization": "<test key>"
    }
]
response1 = oci_openai_client.responses.create(
    model=model,
    input="Please use stirpe create account with a and a@g.com",
    tools=tools,
    store=True
)

print(response1.output)