# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

conversation = oci_openai_client.conversations.create(
    metadata={"topic": "demo"}, items=[{"type": "message", "role": "user", "content": "Hello!"}]
)
print(conversation)
