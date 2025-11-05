# oci-openai

[![PyPI - Version](https://img.shields.io/pypi/v/oci-openai.svg)](https://pypi.org/project/oci-openai)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-openai.svg)](https://pypi.org/project/oci-openai)

**OCI-OpenAI** is a client library jointly maintained by the **Oracle Cloud Infrastructure (OCI) Generative AI** and **OCI Data Science** teams.

This package simplifies integration between **OpenAI’s Python SDK** and Oracle Cloud Infrastructure services — supporting both the **OCI Generative AI Service** and the **OCI Data Science Model Deployment** service.
It provides robust authentication and authorization utilities that allow developers to securely connect to and invoke OCI-hosted large language models (LLMs) using standard OpenAI-compatible APIs.

By leveraging this library, you can:
- Seamlessly connect to **OCI Generative AI** endpoints.
- Interact with **OCI Data Science Model Deployment** LLM endpoints using the same OpenAI-style interface.
- Ensure compliance with OCI security and access control best practices.

---

## Table of Contents

- [oci-openai](#oci-openai)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Examples](#examples)
    - [OCI Generative AI](#oci-generative-ai)
      - [Using the OCI OpenAI Synchronous Client](#using-the-oci-openai-synchronous-client)
      - [Using the OCI OpenAI Asynchronous Client](#using-the-oci-openai-asynchronous-client)
      - [Using the Native OpenAI Client](#using-the-native-openai-client)
    - [OCI Data Science Model Deployment](#oci-data-science-model-deployment)
      - [Using the OCI OpenAI Synchronous Client](#using-the-oci-openai-synchronous-client-1)
      - [Using the OCI OpenAI Asynchronous Client](#using-the-oci-openai-asynchronous-client-1)
      - [Using the Native OpenAI Client](#using-the-native-openai-client-1)
    - [Signers](#signers)
  - [Contributing](#contributing)
  - [Security](#security)
  - [License](#license)

---

## Installation

```console
pip install oci-openai
````

---

## Examples

### OCI Generative AI

#### Using the OCI OpenAI Synchronous Client

```python
from oci_openai import OciOpenAI, OciSessionAuth

client = OciOpenAI(
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    auth=OciSessionAuth(profile_name="<profile name>"),
    compartment_id="<compartment ocid>",
)

completion = client.chat.completions.create(
    model="<model name>",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.model_dump_json())
```

#### Using the OCI OpenAI Asynchronous Client

```python
from oci_openai import AsyncOciOpenAI, OciSessionAuth

client = AsyncOciOpenAI(
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    auth=OciSessionAuth(profile_name="<profile name>"),
    compartment_id="<compartment ocid>",
)

completion = await client.chat.completions.create(
    model="<model name>",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.model_dump_json())
```

#### Using the Native OpenAI Client

```python

import httpx
from openai import OpenAI
from oci_openai import OciSessionAuth

# Example for OCI Data Science Model Deployment endpoint
client = OpenAI(
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.client(auth=OciSessionAuth()),
)

response = client.chat.completions.create(
    model="<model-name>",
    messages=[
        {
            "role": "user",
            "content": "Explain how to list all files in a directory using Python.",
        },
    ],
)
print(response.model_dump_json())
```

---

### OCI Data Science Model Deployment

#### Using the OCI OpenAI Synchronous Client

```python
from oci_openai import OciOpenAI, OciSessionAuth

client = OciOpenAI(
    service_endpoint="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/<OCID>/predict/v1",
    auth=OciSessionAuth(profile_name="<profile name>")
)

response = client.chat.completions.create(
    model="<model-name>",
    messages=[
        {
            "role": "user",
            "content": "Explain how to list all files in a directory using Python.",
        },
    ],
)

print(response.model_dump_json())
```

#### Using the OCI OpenAI Asynchronous Client

```python
from oci_openai import AsyncOciOpenAI, OciSessionAuth

# Example for OCI Data Science Model Deployment endpoint
client = AsyncOciOpenAI(
    service_endpoint="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/<OCID>/predict/v1",
    auth=OciSessionAuth(profile_name="<profile name>")
)

response = await client.chat.completions.create(
    model="<model-name>",
    messages=[
        {
            "role": "user",
            "content": "Explain how to list all files in a directory using Python.",
        },
    ],
)

print(response.model_dump_json())
```


#### Using the Native OpenAI Client

```python

import httpx
from openai import OpenAI
from oci_openai import OciSessionAuth

# Example for OCI Data Science Model Deployment endpoint
client = OpenAI(
    api_key="OCI",
    base_url="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/<OCID>/predict/v1",
    http_client=httpx.client(auth=OciSessionAuth()),
)

response = client.chat.completions.create(
    model="<model-name>",
    messages=[
        {
            "role": "user",
            "content": "Explain how to list all files in a directory using Python.",
        },
    ],
)
print(response.model_dump_json())
```

### Signers

The library supports multiple OCI authentication methods (signers). Choose the one that matches your runtime environment and security posture.

Supported signers
- `OciSessionAuth` — Uses an OCI session token from your local OCI CLI profile.
- `OciResourcePrincipalAuth` — Uses Resource Principal auth.
- `OciInstancePrincipalAuth` — Uses Instance Principal auth. Best for OCI Compute instances with dynamic group policies.
- `OciUserPrincipalAuth` — Uses an OCI user API key. Suitable for service accounts/automation where API keys are managed securely.


Minimal examples of constructing each auth type:

```python
from oci_openai import (
    OciOpenAI,
    OciSessionAuth,
    OciResourcePrincipleAuth,
    OciInstancePrincipleAuth,
    OciUserPrincipleAuth,
)

# 1) Session (local dev; uses ~/.oci/config + session token)
session_auth = OciSessionAuth(profile_name="DEFAULT")

# 2) Resource Principal (OCI services with RP)
rp_auth = OciResourcePrincipleAuth()

# 3) Instance Principal (OCI Compute)
ip_auth = OciInstancePrincipleAuth()

# 4) User Principal (API key in ~/.oci/config)
up_auth = OciUserPrincipleAuth(profile_name="DEFAULT")
```

---

## Contributing

This project welcomes contributions from the community.
Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md).

---

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process.

---

## License

Copyright (c) 2025 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown at
[https://oss.oracle.com/licenses/upl/](https://oss.oracle.com/licenses/upl/)