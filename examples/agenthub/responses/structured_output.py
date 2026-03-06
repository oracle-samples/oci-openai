# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Structured Output example using Pydantic models."""

from pydantic import BaseModel

from examples.agenthub.common import oci_openai_client


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


response = oci_openai_client.responses.parse(
    model="openai.gpt-4.1",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    store=False,
    text_format=CalendarEvent,
)

event = response.output_parsed
print(event)
