# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

updated = oci_openai_client.conversations.update(
    "conv_b485050b69e54a12ae82cb2688a7217d", metadata={"topic": "project-x"}
)
print(updated)
