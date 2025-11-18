from examples.common import oci_openai_client
from rich import print


model = "openai.gpt-4.1"
tools = [
    {
        "type": "mcp",
        "server_label": "deepwiki",
        "require_approval": "never",
    #  "authorization": "12_sk_test_51SFhniEEmUnXltbbsCMqcyZ4LhCvrYM9euoqZ47vAYurryCe84s9LmgJ3f21yFXefqkBOTaAq7Yf3WFa9Vlmcr4r00GjZUQfru",
        "server_url": "https://mcp.deepwiki.com/mcp"
    }
]


# First Request
response1 = oci_openai_client.responses.create(
    model=model,
    input="please tell me structure about facebook/react",
    tools=tools,
    store=False
)
print(response1.output)


