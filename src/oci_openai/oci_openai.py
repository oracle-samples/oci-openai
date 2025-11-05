# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

import logging
from typing import Any, Generator, Mapping, Optional, Type

import httpx
import oci
import requests
from oci.config import DEFAULT_LOCATION, DEFAULT_PROFILE
from openai._base_client import DefaultAsyncHttpxClient, DefaultHttpxClient
from openai._client import AsyncOpenAI, OpenAI, Timeout
from openai._constants import DEFAULT_MAX_RETRIES
from openai._types import NOT_GIVEN, NotGiven
from typing_extensions import override

logger = logging.getLogger(__name__)

OciAuthSigner = Type[oci.signer.AbstractBaseSigner]


class OciOpenAI(OpenAI):
    """
    A custom OpenAI client implementation for Oracle Cloud Infrastructure (OCI).

    This class extends the OpenAI client to work with OCI Generative AI service
    endpoints and OpenAI-compatible OCI Data Science Model Deployment endpoints,
    handling authentication and request signing specific to OCI.

    Attributes:
        service_endpoint (str): The OCI service endpoint URL.
        auth (httpx.Auth): Authentication handler for OCI request signing.
        compartment_id (str | None): Optional OCI compartment OCID for resource isolation.
        timeout (float | Timeout | None | NotGiven): Request timeout configuration.
        max_retries (int): Maximum number of retry attempts for failed requests.
        default_headers (Mapping[str, str] | None): Default HTTP headers.
        default_query (Mapping[str, object] | None): Default query parameters.
    """

    def __init__(
        self,
        *,
        service_endpoint: str,
        auth: httpx.Auth,
        compartment_id: Optional[str] = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        **kwargs: Any,
    ) -> None:
        # Build base_url
        base_url = _build_service_url(service_endpoint=service_endpoint)

        # Only set http client headers if we actually have a compartment_id
        http_client_headers = (
            {"CompartmentId": compartment_id} if compartment_id else None
        )

        super().__init__(
            api_key="<NOTUSED>",
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=DefaultHttpxClient(
                auth=auth,
                headers=http_client_headers,
            ),
            **kwargs,
        )


class AsyncOciOpenAI(AsyncOpenAI):
    """
    An async OpenAI-compatible client for Oracle Cloud Infrastructure (OCI).

    Supports OCI Generative AI service endpoints and OpenAI-compatible
    OCI Data Science Model Deployment endpoints with async/await,
    handling OCI-specific authentication and request signing.

    Attributes:
        service_endpoint (str): OCI service endpoint URL.
        auth (httpx.Auth): Authentication handler for OCI request signing.
        compartment_id (str | None): Optional OCI compartment OCID.
        timeout (float | Timeout | None | NotGiven): Request timeout configuration.
        max_retries (int): Max retry attempts for failed requests.
        default_headers (Mapping[str, str] | None): Default HTTP headers.
        default_query (Mapping[str, object] | None): Default query parameters.
    """

    def __init__(
        self,
        *,
        service_endpoint: str,
        auth: httpx.Auth,
        compartment_id: Optional[str] = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        **kwargs: Any,
    ) -> None:
        # Build base_url
        base_url = _build_service_url(service_endpoint=service_endpoint)

        # Only set http client headers if we actually have a compartment_id
        http_client_headers = (
            {"CompartmentId": compartment_id} if compartment_id else None
        )

        super().__init__(
            api_key="<NOTUSED>",
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=DefaultAsyncHttpxClient(
                auth=auth,
                headers=http_client_headers,
            ),
            **kwargs,
        )


class HttpxOciAuth(httpx.Auth):
    """
    Custom HTTPX authentication class that implements OCI request signing.

    This class handles the authentication flow for HTTPX requests by signing them
    using the OCI Signer, which adds the necessary authentication headers for
    OCI API calls.

    Attributes:
        signer (oci.signer.Signer): The OCI signer instance used for request signing
    """

    def __init__(self, signer: OciAuthSigner):
        self.signer = signer

    @override
    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        # Read the request content to handle streaming requests properly
        try:
            content = request.content
        except httpx.RequestNotRead:
            # For streaming requests, we need to read the content first
            content = request.read()

        req = requests.Request(
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers),
            data=content,
        )
        prepared_request = req.prepare()

        # Sign the request using the OCI Signer
        self.signer.do_request_sign(prepared_request)  # type: ignore

        # Update the original HTTPX request with the signed headers
        request.headers.update(prepared_request.headers)

        yield request


class OciSessionAuth(HttpxOciAuth):
    """
    OCI authentication implementation using session-based authentication.

    This class implements OCI authentication using a session token and private key
    loaded from the OCI configuration file. It's suitable for interactive user sessions.

    Attributes:
        signer (oci.auth.signers.SecurityTokenSigner): OCI signer using session token
    """

    def __init__(
        self, config_file: str = DEFAULT_LOCATION, profile_name: str = DEFAULT_PROFILE
    ):
        config = oci.config.from_file(config_file, profile_name)
        token = self._load_token(config)
        private_key = oci.signer.load_private_key_from_file(config["key_file"])  # type: ignore
        self.signer = oci.auth.signers.SecurityTokenSigner(token, private_key)

    def _load_token(self, config: Mapping[str, Any]) -> str:
        token_file = config["security_token_file"]
        with open(token_file, "r") as f:
            return f.read().strip()


class OciResourcePrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using Resource Principal authentication.

    This class implements OCI authentication using Resource Principal credentials,
    which is suitable for services running within OCI that need to access other
    OCI services.
    """

    def __init__(self):
        self.signer = oci.auth.signers.get_resource_principals_signer()  # type: ignore


class OciInstancePrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using Instance Principal authentication.

    This class implements OCI authentication using Instance Principal credentials,
    which is suitable for compute instances that need to access OCI services.
    """

    def __init__(self, **kwargs: Mapping[str, Any]):
        self.signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner(**kwargs)


class OciUserPrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using user principal authentication.

        This class implements OCI authentication using API Key credentials loaded from
    the OCI configuration file. It's suitable for programmatic access to OCI services.

    Attributes:
        signer (oci.signer.Signer): OCI signer configured with API key credentials
    """

    def __init__(
        self, config_file: str = DEFAULT_LOCATION, profile_name: str = DEFAULT_PROFILE
    ):
        config = oci.config.from_file(config_file, profile_name)
        oci.config.validate_config(config)  # type: ignore

        self.signer = oci.signer.Signer(
            tenancy=config["tenancy"],
            user=config["user"],
            fingerprint=config["fingerprint"],
            private_key_file_location=config.get("key_file"),
            pass_phrase=oci.config.get_config_value_or_default(config, "pass_phrase"),  # type: ignore
            private_key_content=config.get("key_content"),
        )


def _build_service_url(service_endpoint: str) -> str:
    """Constructs the service URL based on the provided endpoint."""

    if not service_endpoint:
        raise ValueError("Service endpoint must be provided.")

    # Normalize
    base_url = service_endpoint.rstrip("/")

    # If it's a Generative AI endpoint, append the inference path
    if "generativeai" in base_url:
        url = f"{base_url}/20231130/actions/v1"
        logger.debug("Detected Generative AI endpoint. Constructed full URL: %s", url)
        return url

    # If it's a Data Science model deployment endpoint, leave as is
    logger.debug(
        "Detected Model Deployment endpoint. Using service endpoint directly: %s",
        base_url,
    )
    return base_url
