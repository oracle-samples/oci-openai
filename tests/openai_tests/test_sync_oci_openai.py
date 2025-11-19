# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

# unit test imports
import json

import pytest

# oci openai sdk imports
from oci_openai import OciOpenAI
from tests.openai_tests.common import auth_instance  # noqa: F401
from tests.openai_tests.common import (
    COMPARTMENT_ID,
    CONVERSATION_STORE_ID,
    MODEL,
    REGION,
    RESPONSE_ID,
    RESPONSES_URL,
    _assert_common,
    _set_mock_create_response,
    _set_mock_create_response_with_fc_tools,
    _set_mock_create_response_with_file_input,
    _set_mock_create_response_with_web_search,
    _set_mock_delete_response,
    _set_mock_get_response,
    function_tools,
)


@pytest.fixture
def oci_openai_client(auth_instance):  # noqa F811
    """Return a ready OciOpenAI client for any auth type."""
    client = OciOpenAI(
        auth=auth_instance,
        compartment_id=COMPARTMENT_ID,
        region=REGION,
        conversation_store_id=CONVERSATION_STORE_ID,
    )
    return client


@pytest.mark.usefixtures("httpx_mock")
def test_create_response_sync(httpx_mock, oci_openai_client):
    # ---- Arrange ----
    _set_mock_create_response(httpx_mock=httpx_mock)

    # ---- Act ----
    result = oci_openai_client.responses.create(model=MODEL, input="Hi")

    # ---- Assert ----
    assert result.output[0].content[0].text == "mocked text"
    _assert_common(httpx_mock=httpx_mock)


@pytest.mark.usefixtures("httpx_mock")
def test_get_response_sync(httpx_mock, oci_openai_client):
    # ---- Arrange ----
    _set_mock_get_response(httpx_mock=httpx_mock, response_id=RESPONSE_ID)

    # ---- Act ----
    result = oci_openai_client.responses.retrieve(response_id=RESPONSE_ID)

    # ---- Assert ----
    assert result.output[0].content[0].text == "mocked retrieved text"
    _assert_common(httpx_mock=httpx_mock)


#
@pytest.mark.usefixtures("httpx_mock")
def test_delete_response_sync(httpx_mock, oci_openai_client):
    # ---- Arrange ----
    _set_mock_delete_response(httpx_mock=httpx_mock, response_id=RESPONSE_ID)

    # ---- Act ----
    oci_openai_client.responses.delete(response_id=RESPONSE_ID)

    # ---- Assert ----
    # check that the DELETE request was made
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    req = requests[0]
    assert req.method == "DELETE"
    assert req.url == f"{RESPONSES_URL}/{RESPONSE_ID}"
    # assert common checks
    _assert_common(httpx_mock=httpx_mock)


@pytest.mark.usefixtures("httpx_mock")
def test_create_response_fc_tools_sync(httpx_mock, oci_openai_client):
    # ---- Arrange ----
    _set_mock_create_response_with_fc_tools(httpx_mock=httpx_mock)

    # ---- Act ----
    result = oci_openai_client.responses.create(model=MODEL, input="Hi", tools=function_tools)

    # ---- Assert ----
    assert result.output[0].type == "function_call"
    assert result.output[0].name == "get_current_weather"
    assert json.loads(result.output[0].arguments)["location"] == "Boston, MA"
    _assert_common(httpx_mock=httpx_mock)


@pytest.mark.usefixtures("httpx_mock")
def test_create_response_file_input_sync(httpx_mock, oci_openai_client):
    # ---- Arrange ----
    _set_mock_create_response_with_file_input(httpx_mock=httpx_mock)

    # ---- Act ----
    result = oci_openai_client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "what is in this file?"},
                    {
                        "type": "input_file",
                        "file_url": "https://www.oracle.com/letters/tr.pdf",
                    },
                ],
            }
        ],
    )

    # ---- Assert ----
    assert result.output[0].type == "message"
    assert (
        result.output[0].content[0].text
        == "The file seems to contain excerpts from a letter to the shareholders"
    )
    _assert_common(httpx_mock=httpx_mock)


@pytest.mark.usefixtures("httpx_mock")
def test_create_response_web_search_sync(httpx_mock, oci_openai_client):
    # ---- Arrange ----
    _set_mock_create_response_with_web_search(httpx_mock=httpx_mock)

    # ---- Act ----
    result = oci_openai_client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search_preview"}],
        input="What was a positive news story from today?",
    )

    # ---- Assert ----
    assert result.output[0].type == "web_search_call"
    assert result.output[1].type == "message"
    assert result.output[1].content[0].type == "output_text"
    _assert_common(httpx_mock=httpx_mock)
