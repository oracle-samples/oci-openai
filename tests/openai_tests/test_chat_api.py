# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import time
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


# Tests for HttpxOciAuth token refresh functionality.
def test_should_refresh_token_returns_true_when_last_refresh_is_none():
    """When _last_refresh is None, _should_refresh_token returns True."""
    with patch("oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()):
        auth = OciResourcePrincipalAuth(refresh_interval=3600)
    auth._last_refresh = None
    assert auth._should_refresh_token() is True


def test_should_refresh_token_returns_false_within_interval():
    """When within refresh_interval, _should_refresh_token returns False."""
    with patch("oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()):
        auth = OciResourcePrincipalAuth(refresh_interval=3600)
    auth._last_refresh = time.time() - 100  # 100 seconds ago
    assert auth._should_refresh_token() is False


def test_should_refresh_token_returns_true_past_interval():
    """When past refresh_interval, _should_refresh_token returns True."""
    with patch("oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()):
        auth = OciResourcePrincipalAuth(refresh_interval=3600)
    auth._last_refresh = time.time() - 3700  # over 1 hour ago
    assert auth._should_refresh_token() is True


def test_refresh_if_needed_calls_refresh_signer_when_interval_elapsed():
    """_refresh_if_needed calls _refresh_signer when token should be refreshed."""
    with patch("oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()):
        auth = OciResourcePrincipalAuth(refresh_interval=0)  # always refresh
    with patch.object(auth, "_refresh_signer") as mock_refresh:
        auth._refresh_if_needed()
        mock_refresh.assert_called_once()


def test_refresh_if_needed_does_not_call_refresh_signer_when_within_interval():
    """_refresh_if_needed does not call _refresh_signer when within interval."""
    with patch("oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()):
        auth = OciResourcePrincipalAuth(refresh_interval=3600)
    auth._last_refresh = time.time()  # just refreshed
    with patch.object(auth, "_refresh_signer") as mock_refresh:
        auth._refresh_if_needed()
        mock_refresh.assert_not_called()


def test_refresh_signer_called_on_resource_principal_refresh():
    """
    OciResourcePrincipalAuth._refresh_signer creates new signer via get_resource_principals_signer.
    """
    mock_signer = MagicMock()
    with patch(
        "oci.auth.signers.get_resource_principals_signer",
        return_value=mock_signer,
    ) as mock_get_signer:
        auth = OciResourcePrincipalAuth(refresh_interval=3600)
        assert auth.signer is mock_signer
        auth._refresh_signer()
        assert mock_get_signer.call_count == 2  # init + _refresh_signer
        assert auth.signer is mock_signer
