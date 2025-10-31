# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from unittest.mock import MagicMock, patch

import httpx
import pytest

from oci_openai import (
    OciInstancePrincipleAuth,
    OciOpenAI,
    OciResourcePrincipleAuth,
    OciSessionAuth,
    OciUserPrincipleAuth,
)

SERVICE_ENDPOINT = "https://fake-oci-endpoint.com"
COMPARTMENT_ID = "ocid1.compartment.oc1..exampleuniqueID"


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
    ), patch(
        "oci.signer.load_private_key_from_file", return_value="dummy_private_key"
    ), patch("oci.auth.signers.SecurityTokenSigner", return_value=MagicMock()), patch(
        "builtins.open", create=True
    ) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = "dummy_token"
        auth = OciSessionAuth()
        client = OciOpenAI(
            service_endpoint=SERVICE_ENDPOINT,
            auth=auth,
            compartment_id=COMPARTMENT_ID,
        )
        return client


def create_oci_openai_client_with_resource_principal_auth():
    with patch(
        "oci.auth.signers.get_resource_principals_signer", return_value=MagicMock()
    ):
        auth = OciResourcePrincipleAuth()
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
        auth = OciInstancePrincipleAuth()
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
        auth = OciUserPrincipleAuth()
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
    route = respx_mock.post(f"{SERVICE_ENDPOINT}/20231130/actions/v1/completions").mock(
        return_value=httpx.Response(200, json={"result": "ok"})
    )
    client.completions.create(model="test-model", prompt="hello")
    assert route.called
    sent_headers = route.calls[0].request.headers
    assert sent_headers["compartmentId"] == COMPARTMENT_ID
    assert str(route.calls[0].request.url).startswith(SERVICE_ENDPOINT)
