# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Reasoning examples - effort control and summary output."""

import json

from examples.agenthub.common import client

# Reasoning with effort control
response = client.responses.create(
    model="openai.gpt-5",
    input="What is the answer to 12 * (3 + 9)?",
    reasoning={"effort": "high"},
    store=False,
)
print("Reasoning effort output:")
print(json.dumps(response.to_dict()["output"], indent=4))

# Reasoning with detailed summary
response = client.responses.create(
    model="openai.gpt-5",
    input="What is the answer to 12 * (3 + 9)?",
    reasoning={"summary": "detailed"},
    store=False,
)
print("\nReasoning summary output:")
print(json.dumps(response.to_dict()["output"], indent=4))
