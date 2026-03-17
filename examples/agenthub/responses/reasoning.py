# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Reasoning examples - effort control and summary output."""

from examples.agenthub.common import client


prompt = """
Write a bash script that takes a matrix represented as a string with
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.responses.create(
    model="openai.gpt-oss-120b",
    input=prompt,
    reasoning={"effort": "medium", "summary": "detailed"},
    stream=True,
)
for event in response:
    if event.type == "response.reasoning_summary_part.added":
        print("Thinking...")
    if event.type == "response.reasoning_summary_text.delta":
        print(event.delta, end="", flush=True)
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
print()