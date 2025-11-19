# oci-openai

[![PyPI - Version](https://img.shields.io/pypi/v/oci-openai.svg)](https://pypi.org/project/oci-openai)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-openai.svg)](https://pypi.org/project/oci-openai)

The **OCI OpenAI** Python library provides secure and convenient access to the OpenAI-compatible REST API hosted by **OCI Generative AI Service** and **OCI Data Science Model Deployment** Service.

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
      - [Using with Langchain](#using-with-langchain-openai)
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
    auth=OciSessionAuth(profile_name="<profile name>"),
    region="us-chicago-1",
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
from oci_openai import OciUserPrincipalAuth

# Example for OCI Generative AI endpoint
client = OpenAI(
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name="DEFAULT"),
        headers={"opc-compartment-id": COMPARTMENT_ID}
    ),
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

#### Using with langchain-openai

```python
from langchain_openai import ChatOpenAI
import httpx
from oci_openai import OciUserPrincipalAuth
import os


COMPARTMENT_ID=os.getenv("OCI_COMPARTMENT_ID", "<compartment_id>")

llm = ChatOpenAI(
    model="<model-name>",  # for example "xai.grok-4-fast-reasoning"
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name="DEFAULT"),
        headers={"CompartmentId": COMPARTMENT_ID}
    ),
    # use_responses_api=True
    # stream_usage=True,
    # temperature=None,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg)
```

---

### OCI Data Science Model Deployment

#### Using the OCI OpenAI Synchronous Client

```python
from oci_openai import OciOpenAI, OciSessionAuth

client = OciOpenAI(
    base_url="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/<OCID>/predict/v1",
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
    base_url="https://modeldeployment.us-ashburn-1.oci.customer-oci.com/<OCID>/predict/v1",
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
    http_client=httpx.Client(auth=OciSessionAuth()),
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
    OciResourcePrincipalAuth,
    OciInstancePrincipalAuth,
    OciUserPrincipalAuth,
)

# 1) Session (local dev; uses ~/.oci/config + session token)
session_auth = OciSessionAuth(profile_name="DEFAULT")

# 2) Resource Principal (OCI services with RP)
rp_auth = OciResourcePrincipalAuth()

# 3) Instance Principal (OCI Compute)
ip_auth = OciInstancePrincipalAuth()

# 4) User Principal (API key in ~/.oci/config)
up_auth = OciUserPrincipalAuth(profile_name="DEFAULT")
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
