from rich import print

from examples.common import oci_openai_client

updated = oci_openai_client.conversations.update(
    "conv_b485050b69e54a12ae82cb2688a7217d", metadata={"topic": "project-x"}
)
print(updated)
