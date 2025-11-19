# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from fc_tools import fc_tools
from rich import print

from examples.common import oci_openai_client

model = "openai.gpt-4.1"

# parrel_call
response = oci_openai_client.responses.create(
    model=model,
    input="what is the weather in seattle and in new York?",
    previous_response_id=None,  # root of the history
    tools=fc_tools,
)
print(response.output)


# no parrel_call

response = oci_openai_client.responses.create(
    model=model,
    input="what is the weather in seattle and in new York?",
    previous_response_id=None,  # root of the history
    tools=fc_tools,
    parallel_tool_calls=False,
)
print(response.output)
