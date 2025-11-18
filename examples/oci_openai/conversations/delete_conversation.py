from rich import print

from examples.common import oci_openai_client

deleted = oci_openai_client.conversations.delete("conv_b485050b69e54a12ae82cb2688a7217d")
print(deleted)
