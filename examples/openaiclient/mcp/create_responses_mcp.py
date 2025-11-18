from examples.common import oci_openai_client
from rich import print

  #  "authorization": "12_sk_test_51SFhniEEmUnXltbbsCMqcyZ4LhCvrYM9euoqZ47vAYurryCe84s9LmgJ3f21yFXefqkBOTaAq7Yf3WFa9Vlmcr4r00GjZUQfru",
   

model = "openai.gpt-4.1"
tools = [
    {
        "type": "mcp",
        "server_label": "deepwiki",
        "require_approval": "always",
        "server_url": "https://mcp.deepwiki.com/mcp"
    }
]
response1 = oci_openai_client.responses.create(
    model=model,
    input="please tell me structure about facebook/react",
    tools=tools,
    store=True
)

print(response1.output)

approve_id = response1.output[1].id
id = response1.id

approval_response = {
    "type": "mcp_approval_response",
    "approval_request_id": approve_id,
    "approve": True
}


response2 = oci_openai_client.responses.create(
    model=model,
    input=[approval_response],
    tools=tools,
    previous_response_id=id
)
print(response2.output)
