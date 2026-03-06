# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import warnings
from unittest.mock import MagicMock, patch

import pytest

from oci_openai import AsyncOciOpenAI, OciOpenAI, OciSessionAuth

PROJECT_ID = "ocid1.generativeaiproject.oc1.us-chicago-1.dummy"
COMPARTMENT_ID = "ocid1.compartment.oc1..dummy"
CONVERSATION_STORE_ID = "ocid1.generativeaiconversationstore.oc1..dummy"
REGION = "us-chicago-1"


@pytest.fixture
def mock_session_auth():
    with (
        patch(
            "oci.config.from_file",
            return_value={
                "user": "ocid1.user.oc1..dummy",
                "fingerprint": "dummyfp",
                "key_file": "/fake/key.pem",
                "tenancy": "ocid1.tenancy.oc1..dummy",
                "region": "us-chicago-1",
                "security_token_file": "/fake/token",
            },
        ),
        patch.object(OciSessionAuth, "_load_token", return_value="fake_token_string"),
        patch.object(OciSessionAuth, "_load_private_key", return_value="fake_private_key_data"),
        patch("oci.auth.signers.SecurityTokenSigner", return_value=MagicMock()),
    ):
        yield OciSessionAuth(profile_name="DEFAULT")


def test_project_param_creates_client(mock_session_auth):
    client = OciOpenAI(
        auth=mock_session_auth,
        region=REGION,
        project=PROJECT_ID,
    )
    assert client.project == PROJECT_ID


def test_project_param_creates_async_client(mock_session_auth):
    client = AsyncOciOpenAI(
        auth=mock_session_auth,
        region=REGION,
        project=PROJECT_ID,
    )
    assert client.project == PROJECT_ID


def test_compartment_id_emits_deprecation_warning(mock_session_auth):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        OciOpenAI(
            auth=mock_session_auth,
            region=REGION,
            compartment_id=COMPARTMENT_ID,
        )
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) >= 1
        assert "compartment_id is deprecated" in str(deprecation_warnings[0].message)


def test_conversation_store_id_emits_deprecation_warning(mock_session_auth):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        OciOpenAI(
            auth=mock_session_auth,
            region=REGION,
            compartment_id=COMPARTMENT_ID,
            conversation_store_id=CONVERSATION_STORE_ID,
        )
        conv_warnings = [
            x
            for x in w
            if issubclass(x.category, DeprecationWarning)
            and "conversation_store_id" in str(x.message)
        ]
        assert len(conv_warnings) >= 1


def test_no_project_no_compartment_raises_error(mock_session_auth):
    with pytest.raises(ValueError, match="project"):
        OciOpenAI(
            auth=mock_session_auth,
            region=REGION,
        )


def test_project_no_deprecation_warning(mock_session_auth):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        OciOpenAI(
            auth=mock_session_auth,
            region=REGION,
            project=PROJECT_ID,
        )
        deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(deprecation_warnings) == 0


def test_data_science_endpoint_no_project_required(mock_session_auth):
    client = OciOpenAI(
        auth=mock_session_auth,
        base_url="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/ocid/predict/v1",
    )
    assert client is not None
