# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

# unit test imports
import pytest
from agents import Agent, Runner, set_default_openai_client

# oci openai sdk imports
from oci_openai import AsyncOciOpenAI
from tests.openai_agents_tests.common import auth_instance  # noqa: F401
from tests.openai_agents_tests.common import (
    COMPARTMENT_ID,
    CONVERSATION_STORE_ID,
    MODEL,
    REGION,
    _assert_common,
    _set_mock_create_response,
)


@pytest.fixture
def oci_async_openai_client(auth_instance):  # noqa F811
    """Return a ready OciOpenAI client for any auth type."""
    client = AsyncOciOpenAI(
        auth=auth_instance,
        compartment_id=COMPARTMENT_ID,
        region=REGION,
        conversation_store_id=CONVERSATION_STORE_ID,
    )
    return client


@pytest.mark.asyncio
@pytest.mark.usefixtures("httpx_mock")
async def test_agent_response(httpx_mock, oci_async_openai_client):
    # ---- Arrange ----
    _set_mock_create_response(httpx_mock=httpx_mock)
    # ---- Act ----
    set_default_openai_client(oci_async_openai_client)
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=MODEL,
    )
    result = await Runner.run(agent, "Hi")
    # ---- Assert ----
    assert result.final_output == "mocked text"
    _assert_common(httpx_mock=httpx_mock)
