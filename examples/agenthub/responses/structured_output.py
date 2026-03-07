# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Structured Output example using Pydantic models."""

from pydantic import BaseModel

from examples.agenthub.common import client


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


response = client.responses.parse(
    model="xai.grok-4-1-fast-reasoning",
    input=[
        {
          "role": "system",
          "content": "Extract the event information.",
        },
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
