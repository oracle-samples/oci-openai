# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from unittest.mock import MagicMock, patch

import pytest
from httpx import Request

from oci_openai import OciInstancePrincipalAuth, OciResourcePrincipalAuth, OciSessionAuth
from oci_openai.oci_openai import (
    COMPARTMENT_ID_HEADER,
    CONVERSATION_STORE_ID_HEADER,
    _build_base_url,
    _build_service_endpoint,
)

COMPARTMENT_ID = "ocid1.compartment.oc1..dummy"
CONVERSATION_STORE_ID = "ocid1.generativeaiconversationstore.oc1..dummy"
REGION = "us-chicago-1"
MODEL = "openai.gpt-4o"
SESSION_PRINCIPAL = "session_principal"
RESOURCE_PRINCIPAL = "resource_principal"
INSTANCE_PRINCIPAL = "instance_principal"
BASE_URL = _build_base_url(_build_service_endpoint(region="us-chicago-1"))
RESPONSES_URL = f"{BASE_URL}/responses"
RESPONSE_ID = "resp_123"


# Fixtures
@pytest.fixture(
    params=[
        (SESSION_PRINCIPAL, OciSessionAuth, {"profile_name": "DEFAULT"}),
        (RESOURCE_PRINCIPAL, OciResourcePrincipalAuth, {}),
        (INSTANCE_PRINCIPAL, OciInstancePrincipalAuth, {}),
    ],
    ids=[SESSION_PRINCIPAL, RESOURCE_PRINCIPAL, INSTANCE_PRINCIPAL],
)
def auth_instance(request):
    name, auth_class, kwargs = request.param

    def set_signer(signer_name: str):
        dummy_signer = MagicMock()
        patcher = patch(signer_name, return_value=dummy_signer)
        patcher.start()
        request.addfinalizer(patcher.stop)
        kwargs["signer"] = dummy_signer

    if name == RESOURCE_PRINCIPAL:
        set_signer(signer_name="oci.auth.signers.get_resource_principals_signer")
    elif name == INSTANCE_PRINCIPAL:
        set_signer(signer_name="oci.auth.signers.InstancePrincipalsSecurityTokenSigner")
    elif name == "session_principal":
        # --- Patch config + signer + token/private_key loading ---
        patch_config = patch(
            "oci.config.from_file",
            return_value={
                "user": "ocid1.user.oc1..dummy",
                "fingerprint": "dummyfp",
                "key_file": "/fake/key.pem",
                "tenancy": "ocid1.tenancy.oc1..dummy",
                "region": "us-chicago-1",
                "security_token_file": "/fake/token",
            },
        )
        patch_token = patch.object(OciSessionAuth, "_load_token", return_value="fake_token_string")
        patch_private_key = patch.object(
            OciSessionAuth, "_load_private_key", return_value="fake_private_key_data"
        )
        patch_signer = patch("oci.auth.signers.SecurityTokenSigner", return_value=MagicMock())

        # Start all patches
        for p in [patch_config, patch_token, patch_private_key, patch_signer]:
            p.start()
            request.addfinalizer(p.stop)

    return auth_class(**kwargs)


def _assert_common(httpx_mock):
    last_request: Request = httpx_mock.get_requests()[0]
    assert "Authorization" in last_request.headers
    assert last_request.headers.get(COMPARTMENT_ID_HEADER) == COMPARTMENT_ID
    assert last_request.headers.get(CONVERSATION_STORE_ID_HEADER) == CONVERSATION_STORE_ID


function_tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location", "unit"],
        },
    }
]


def _set_mock_create_response(httpx_mock):
    httpx_mock.add_response(
        url=RESPONSES_URL,
        method="POST",
        json={"id": RESPONSE_ID, "output": [{"content": [{"text": "mocked text"}]}]},
        status_code=200,
    )


def _set_mock_get_response(httpx_mock, response_id: str):
    httpx_mock.add_response(
        url=f"{RESPONSES_URL}/{response_id}",
        method="GET",
        json={
            "id": response_id,
            "output": [{"content": [{"text": "mocked retrieved text"}]}],
        },
        status_code=200,
    )


def _set_mock_delete_response(httpx_mock, response_id: str):
    httpx_mock.add_response(
        url=f"{RESPONSES_URL}/{response_id}",
        method="DELETE",
        status_code=200,
    )


def _set_mock_create_response_with_fc_tools(httpx_mock):
    httpx_mock.add_response(
        url=RESPONSES_URL,
        method="POST",
        json={
            "id": RESPONSE_ID,
            "output": [
                {
                    "type": "function_call",
                    "id": "fc_67ca09c6bedc8190a7abfec07b1a1332096610f474011cc0",
                    "call_id": "call_unLAR8MvFNptuiZK6K6HCy5k",
                    "name": "get_current_weather",
                    "arguments": '{"location":"Boston, MA","unit":"celsius"}',
                    "status": "completed",
                }
            ],
            "tools": function_tools,
        },
        status_code=200,
    )


def _set_mock_create_response_with_file_input(httpx_mock):
    httpx_mock.add_response(
        url=RESPONSES_URL,
        method="POST",
        json={
            "id": RESPONSE_ID,
            "output": [
                {
                    "id": "msg_686ee",
                    "type": "message",
                    "status": "completed",
                    "content": [
                        {
                            "type": "output_text",
                            "annotations": [],
                            "logprobs": [],
                            "text": "The file seems to contain excerpts "
                            "from a letter to the shareholders",
                        }
                    ],
                    "role": "assistant",
                }
            ],
        },
        status_code=200,
    )


def _set_mock_create_response_with_web_search(httpx_mock):
    httpx_mock.add_response(
        url=RESPONSES_URL,
        method="POST",
        json={
            "id": RESPONSE_ID,
            "output": [
                {"type": "web_search_call", "id": "ws_67cc", "status": "completed"},
                {
                    "type": "message",
                    "id": "msg_67cc",
                    "status": "completed",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": "As of today, Oct 7, 2025, "
                            "one notable positive news story...",
                            "annotations": [
                                {
                                    "type": "url_citation",
                                    "start_index": 442,
                                    "end_index": 557,
                                    "url": "https://.../?utm_source=chatgpt.com",
                                    "title": "...",
                                },
                                {
                                    "type": "url_citation",
                                    "start_index": 962,
                                    "end_index": 1077,
                                    "url": "https://.../?utm_source=chatgpt.com",
                                    "title": "...",
                                },
                            ],
                        }
                    ],
                },
            ],
        },
        status_code=200,
    )
