from examples.common import oci_openai_client
from rich import print

conversation = oci_openai_client.conversations.retrieve("conv_b485050b69e54a12ae82cb2688a7217d")
print(conversation)