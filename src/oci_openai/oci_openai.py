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

API_KEY = "<NOTUSED>"
COMPARTMENT_ID_HEADER = "CompartmentId"
OPC_COMPARTMENT_ID_HEADER = "opc-compartment-id"
CONVERSATION_STORE_ID_HEADER = "opc-conversation-store-id"


class OciOpenAI(OpenAI):
    """
    A custom OpenAI client implementation for Oracle Cloud Infrastructure (OCI).

    This class extends the OpenAI client to work with OCI Generative AI service
    endpoints and OpenAI-compatible OCI Data Science Model Deployment endpoints,
    handling authentication and request signing specific to OCI.

    Attributes:
        auth (httpx.Auth): Authentication handler for OCI request signing.
        region (str | None): The OCI service region, e.g., 'us-chicago-1'.
                             Must be provided if service_endpoint and base_url are None
        service_endpoint (str | None): The OCI service endpoint. when service_endpoint
                                       provided, the region will be ignored.
        base_url (str | None): The OCI service full path URL. when base_url provided, the region
                               and service_endpoint will be ignored.
        compartment_id (str | None): OCI compartment OCID for resource isolation, required for
                                     Generative AI Service, Optional for Data Science Service
        timeout (float | Timeout | None | NotGiven): Request timeout configuration.
        max_retries (int): Maximum number of retry attempts for failed requests.
        default_headers (Mapping[str, str] | None): Default HTTP headers.
        default_query (Mapping[str, object] | None): Default query parameters.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth,
        region: str = None,
        service_endpoint: str = None,
        base_url: str = None,
        compartment_id: str = None,
        conversation_store_id: Optional[str] = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        **kwargs: Any,
    ) -> None:
        base_url = _resolve_base_url(region, service_endpoint, base_url)

        if "generativeai" in base_url and not compartment_id:
            raise ValueError(
                "The compartment_id is required to access the OCI Generative AI Service."
            )
        http_client_headers = _build_headers(compartment_id, conversation_store_id)

        super().__init__(
            api_key=API_KEY,
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
        auth (httpx.Auth): Authentication handler for OCI request signing.
        region (str | None): The OCI service region, e.g., 'us-chicago-1'.
                             Must be provided if service_endpoint and base_url are None
        service_endpoint (str | None): The OCI service endpoint. when service_endpoint
                                       provided, the region will be ignored.
        base_url (str | None): The OCI service full path URL. when base_url provided, the region
                               and service_endpoint will be ignored.
        compartment_id (str | None): OCI compartment OCID for resource isolation, required for
                                     Generative AI Service, Optional for Data Science Service
        timeout (float | Timeout | None | NotGiven): Request timeout configuration.
        max_retries (int): Max retry attempts for failed requests.
        default_headers (Mapping[str, str] | None): Default HTTP headers.
        default_query (Mapping[str, object] | None): Default query parameters.
    """

    def __init__(
        self,
        *,
        auth: httpx.Auth,
        region: str = None,
        service_endpoint: str = None,
        base_url: str = None,
        compartment_id: Optional[str] = None,
        conversation_store_id: Optional[str] = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        **kwargs: Any,
    ) -> None:
        base_url = _resolve_base_url(region, service_endpoint, base_url)

        if "generativeai" in base_url and not compartment_id:
            raise ValueError(
                "The compartment_id is required to access the OCI Generative AI Service."
            )
        http_client_headers = _build_headers(compartment_id, conversation_store_id)

        super().__init__(
            api_key=API_KEY,
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
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
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
        self,
        config_file: str = DEFAULT_LOCATION,
        profile_name: str = DEFAULT_PROFILE,
        **kwargs: Mapping[str, Any],
    ):
        """
        Initialize a Security Token-based OCI signer.

        Parameters
        ----------
        config_file : str, optional
            Path to the OCI configuration file. Defaults to `~/.oci/config`.
        profile_name : str, optional
            Profile name inside the OCI configuration file to use.
            Defaults to "DEFAULT".
        **kwargs : Mapping[str, Any]
            Optional keyword arguments:
              - `generic_headers`: Optional[Dict[str, str]]
                    Headers to be used for generic requests.
                    Default: `["date", "(request-target)", "host"]`
              - `body_headers`: Optional[Dict[str, str]]
                    Headers to be used for signed request bodies.
                    Default: `["content-length", "content-type", "x-content-sha256"]`

        Raises
        ------
        oci.exceptions.ConfigFileNotFound
            If the configuration file cannot be found.
        KeyError
            If a required key such as `"key_file"` is missing in the config.
        Exception
            For any other initialization errors.
        """
        # Load OCI configuration and token
        config = oci.config.from_file(config_file, profile_name)
        token = self._load_token(config)

        # Load the private key from config
        key_path = config.get("key_file")
        if not key_path:
            raise KeyError(f"Missing 'key_file' entry in OCI config profile '{profile_name}'.")
        private_key = self._load_private_key(config)

        # Optional signer header customization
        generic_headers = kwargs.pop("generic_headers", None)
        body_headers = kwargs.pop("body_headers", None)

        additional_kwargs = {}
        if generic_headers:
            additional_kwargs["generic_headers"] = generic_headers
        if body_headers:
            additional_kwargs["body_headers"] = body_headers

        self.signer = oci.auth.signers.SecurityTokenSigner(token, private_key, **additional_kwargs)

    def _load_token(self, config: Mapping[str, Any]) -> str:
        token_file = config["security_token_file"]
        with open(token_file, "r") as f:
            return f.read().strip()

    def _load_private_key(self, config: Any) -> str:
        return oci.signer.load_private_key_from_file(config["key_file"])


class OciResourcePrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using Resource Principal authentication.

    This class implements OCI authentication using Resource Principal credentials,
    which is suitable for services running within OCI that need to access other
    OCI services.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(signer=oci.auth.signers.get_resource_principals_signer(**kwargs))


class OciInstancePrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using Instance Principal authentication.

    This class implements OCI authentication using Instance Principal credentials,
    which is suitable for compute instances that need to access OCI services.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(signer=oci.auth.signers.InstancePrincipalsSecurityTokenSigner(**kwargs))


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
    ) -> None:
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


def _build_service_endpoint(region: str) -> str:
    return f"https://inference.generativeai.{region}.oci.oraclecloud.com"


def _build_base_url(service_endpoint: str) -> str:
    url = service_endpoint.rstrip(" /")
    return f"{url}/openai/v1"


def _resolve_base_url(region: str = None, service_endpoint: str = None, base_url: str = None):
    # build service endpoint by region when service_endpoint is empty,
    # then build base url from service endpoint
    if not base_url and not service_endpoint and not region:
        raise ValueError("Region or service endpoint or base url must be provided.")
    base_url = (
        base_url
        if base_url
        else _build_base_url(
            service_endpoint if service_endpoint else _build_service_endpoint(region)
        )
    )
    return base_url


def _build_headers(compartment_id: str = None, conversation_store_id: str = None):
    http_client_headers = (
        {
            COMPARTMENT_ID_HEADER: compartment_id,  # for backward compatibility
            OPC_COMPARTMENT_ID_HEADER: compartment_id,
        }
        if compartment_id
        else {}
    )
    if conversation_store_id:
        http_client_headers[CONVERSATION_STORE_ID_HEADER] = conversation_store_id
    return http_client_headers
