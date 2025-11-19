# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from unittest.mock import MagicMock, patch

import httpx
import pytest

from oci_openai import (
    OciInstancePrincipalAuth,
    OciOpenAI,
    OciResourcePrincipalAuth,
    OciSessionAuth,
    OciUserPrincipalAuth,
)
from oci_openai.oci_openai import (
    _build_base_url,
    _build_headers,
    _build_service_endpoint,
    _resolve_base_url,
)

SERVICE_ENDPOINT = "https://generativeai.fake-oci-endpoint.com"
COMPARTMENT_ID = "ocid1.compartment.oc1..exampleuniqueID"
CONVERSATION_STORE_ID = "ocid1.generativeaiconversationstore.oc1..exampleID"


def create_oci_openai_client_with_session_auth():
    with patch(
        "oci.config.from_file",
        return_value={
            "key_file": "dummy.key",
            "security_token_file": "dummy.token",
            "tenancy": "dummy_tenancy",
            "user": "dummy_user",
            "fingerprint": "dummy_fingerprint",
        },
    ), patch("oci.signer.load_private_key_from_file", return_value="dummy_private_key"), patch(
        "oci.auth.signers.SecurityTokenSigner", return_value=MagicMock()
    ), patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy_token"
        auth = OciSessionAuth()
        client = OciOpenAI(
            service_endpoint=SERVICE_ENDPOINT,
            auth=auth,
            compartment_id=COMPARTMENT_ID,
        )
        return client


def create_oci_openai_client_with_resource_principal_auth():
    with patch("oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()):
        auth = OciResourcePrincipalAuth()
        client = OciOpenAI(
            service_endpoint=SERVICE_ENDPOINT,
            auth=auth,
            compartment_id=COMPARTMENT_ID,
        )
        return client


def create_oci_openai_client_with_instance_principal_auth():
    with patch(
        "oci.auth.signers.InstancePrincipalsSecurityTokenSigner",
        return_value=MagicMock(),
    ):
        auth = OciInstancePrincipalAuth()
        client = OciOpenAI(
            service_endpoint=SERVICE_ENDPOINT,
            auth=auth,
            compartment_id=COMPARTMENT_ID,
        )
        return client


def create_oci_openai_client_with_user_principal_auth():
    with patch(
        "oci.config.from_file",
        return_value={
            "key_file": "dummy.key",
            "tenancy": "dummy_tenancy",
            "user": "dummy_user",
            "fingerprint": "dummy_fingerprint",
        },
    ), patch("oci.config.validate_config", return_value=True), patch(
        "oci.signer.Signer", return_value=MagicMock()
    ):
        auth = OciUserPrincipalAuth()
        client = OciOpenAI(
            service_endpoint=SERVICE_ENDPOINT,
            auth=auth,
            compartment_id=COMPARTMENT_ID,
        )
        return client


auth_client_factories = [
    create_oci_openai_client_with_session_auth,
    create_oci_openai_client_with_resource_principal_auth,
    create_oci_openai_client_with_instance_principal_auth,
    create_oci_openai_client_with_user_principal_auth,
]


@pytest.mark.parametrize("client_factory", auth_client_factories)
@pytest.mark.respx()
def test_oci_openai_auth_headers(client_factory, respx_mock):
    client = client_factory()
    route = respx_mock.post(f"{SERVICE_ENDPOINT}/openai/v1/completions").mock(
        return_value=httpx.Response(200, json={"result": "ok"})
    )
    client.completions.create(model="test-model", prompt="hello")
    assert route.called
    sent_headers = route.calls[0].request.headers
    assert sent_headers["CompartmentId"] == COMPARTMENT_ID
    assert sent_headers["opc-compartment-id"] == COMPARTMENT_ID
    assert str(route.calls[0].request.url).startswith(SERVICE_ENDPOINT)


def test_build_service_endpoint():
    """Test that the function resolve Generative AI service endpoint by region."""
    result = _build_service_endpoint("us-chicago-1")
    assert result == "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"


def test_build_base_url():
    """Test that the function appends the inference path for Generative AI endpoints."""
    endpoint = "https://ppe.inference.generativeai.us-chicago-1.oci.oraclecloud.com"
    result = _build_base_url(service_endpoint=endpoint)
    assert result == f"{endpoint}/openai/v1"


def test_resolve_base_url():
    with pytest.raises(ValueError):
        _resolve_base_url()

    url = "https://datascience.us-phoenix-1.oci.oraclecloud.com/20190101/actions/invokeEndpoint"
    result = _resolve_base_url(region="any", service_endpoint="any", base_url=url)
    assert result == url

    expected_url = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1"
    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
    result = _resolve_base_url(region="any", service_endpoint=endpoint)
    assert result == expected_url

    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/ //"
    result = _resolve_base_url(region="any", service_endpoint=endpoint)
    assert result == expected_url

    result = _resolve_base_url("us-chicago-1")
    assert result == expected_url


def test_build_headers():
    result = _build_headers()
    assert len(result) == 0

    result = _build_headers(None, CONVERSATION_STORE_ID)
    assert "CompartmentId" not in result
    assert "opc-compartment-id" not in result
    assert result["opc-conversation-store-id"] == CONVERSATION_STORE_ID

    result = _build_headers(COMPARTMENT_ID, None)
    assert result["CompartmentId"] == COMPARTMENT_ID
    assert result["opc-compartment-id"] == COMPARTMENT_ID
    assert "opc-conversation-store-id" not in result

    result = _build_headers(COMPARTMENT_ID, CONVERSATION_STORE_ID)
    assert result["CompartmentId"] == COMPARTMENT_ID
    assert result["opc-compartment-id"] == COMPARTMENT_ID
    assert result["opc-conversation-store-id"] == CONVERSATION_STORE_ID
