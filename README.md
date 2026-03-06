# oci-openai

[![PyPI - Version](https://img.shields.io/pypi/v/oci-openai.svg)](https://pypi.org/project/oci-openai)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-openai.svg)](https://pypi.org/project/oci-openai)

The **OCI OpenAI** Python library provides secure and convenient access to the OpenAI-compatible REST API hosted by **OCI Generative AI Service** and **OCI Data Science Model Deployment** Service.

---

## Table of Contents

- [oci-openai](#oci-openai)
  - [Table of Contents](#table-of-contents)
  - [Before You Start](#before-you-start)
  - [Installation](#installation)
  - [Agentic API (GA)](#agentic-api-ga)
    - [Quickstart with API Key](#quickstart-with-api-key)
    - [Quickstart with OCI IAM](#quickstart-with-oci-iam)
    - [Using the OciOpenAI Client](#using-the-ociopenai-client)
    - [Migration from LA to GA](#migration-from-la-to-ga)
  - [Agent Hub Examples](#agent-hub-examples)
  - [Examples (Legacy / Chat Completions)](#examples-legacy--chat-completions)
    - [OCI Generative AI](#oci-generative-ai)
    - [OCI Data Science Model Deployment](#oci-data-science-model-deployment)
    - [Signers](#signers)
  - [Contributing](#contributing)
  - [Security](#security)
  - [License](#license)

---

## Before you start

**Important!**

Note that this package, as well as API keys package described below, only supports OpenAI, xAi Grok and Meta LLama models on OCI Generative AI.

Before you start using this package, determine if this is the right option for you.

If you are looking for a seamless way to port your code from an OpenAI compatible endpoint to OCI Generative AI endpoint, and you are currently using OpenAI-style API keys, you might want to use [OCI Generative AI API Keys](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm) instead.

With OCI Generative AI API Keys, use the native `openai` SDK like before. Just update the `base_url`, create API keys in your OCI console, insure the policy granting the key access to generative AI services is present and you are good to go.

- Create an API key in Console: **Generative AI** -> **API Keys**
- Create a security policy: **Identity & Security** -> **Policies**

To authorize a specific API Key
```
allow any-user to use generative-ai-family in compartment <compartment-name> where ALL { request.principal.type='generativeaiapikey', request.principal.id='ocid1.generativeaiapikey.oc1.us-chicago-1....' }
```

To authorize any API Key
```
allow any-user to use generative-ai-family in compartment <compartment-name> where ALL { request.principal.type='generativeaiapikey' }
```

- Update the `base_url` in your code:

```python
from openai import OpenAI
import os

API_KEY=os.getenv("OPENAI_API_KEY")

print(API_KEY)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1"
)

# Responses API
response = client.responses.create(
    model="openai.gpt-oss-120b",
    # model="xai.grok-3",
    # meta models are not supported with the Responses API
    input="Write a one-sentence bedtime story about a unicorn."
)
print(response)

# Completion API
response = client.chat.completions.create(
    # model="openai.gpt-oss-120b",
    # model="meta.llama-3.3-70b-instruct",
    model="xai.grok-3",
    messages=[{
        "role": "user", 
        "content": "Write a one-sentence bedtime story about a unicorn."
        }
    ]
)
print(response)
```


API Keys offer a seamless transition from code using the openai SDK, and allow usage in 3rd party code or services that don't offer an override of the http client.

However, if authentication at the user, compute instance, resource or workload level (OKE pods) is preferred, this package is for you.

It offers the same compatibility with the `openai` SDK, but requires patching the http client. See the following instruction on how to use it.

## Installation

```console
pip install oci-openai
```

---

## Agentic API (GA)

The OCI Generative AI Platform **Agentic API** is a unified, OpenAI Responses-compatible API for building agents. It supports multiple model providers (GPT, Grok, Gemini, GPT-OSS), platform-managed tools (web search, file search, code interpreter, MCP, image generation), conversation memory, and more — all under unified OCI auth, billing, and governance.

In GA, a **Generative AI Project** replaces the previous `compartment_id` and `conversation_store_id` parameters. Create a project in the OCI Console, then pass its OCID via the `project` parameter.

### Quickstart with API Key

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # your API Key
    project="ocid1.generativeaiproject.oc1.us-chicago-1.xxxxxxxx",  # your Project OCID
)

response = client.responses.create(
    model="openai.gpt-4.1",
    input="What is 2x2?",
)
print(response.output_text)
```

### Quickstart with OCI IAM

```python
import httpx
from openai import OpenAI
from oci_openai import OciSessionAuth

client = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1",
    api_key="not-used",
    project="ocid1.generativeaiproject.oc1.us-chicago-1.xxxxxxxx",  # your Project OCID
    http_client=httpx.Client(auth=OciSessionAuth(profile_name="DEFAULT")),
)

response = client.responses.create(
    model="openai.gpt-4.1",
    input="What is 2x2?",
)
print(response.output_text)
```

### Using the OciOpenAI Client

The `OciOpenAI` client now accepts a `project` parameter directly:

```python
from oci_openai import OciOpenAI, OciSessionAuth

client = OciOpenAI(
    auth=OciSessionAuth(profile_name="DEFAULT"),
    region="us-chicago-1",
    project="ocid1.generativeaiproject.oc1.us-chicago-1.xxxxxxxx",
)

response = client.responses.create(
    model="openai.gpt-4.1",
    input="What is 2x2?",
)
print(response.output_text)
```

### Migration from LA to GA

| Before (LA) | After (GA) |
|---|---|
| `compartment_id="ocid1.compartment..."` | `project="ocid1.generativeaiproject..."` |
| `conversation_store_id="ocid1.generativeaiconversationstore..."` | `project="ocid1.generativeaiproject..."` |

Both `compartment_id` and `conversation_store_id` still work during the migration grace period but emit deprecation warnings.

---

## Agent Hub Examples

The [`examples/agenthub/`](./examples/agenthub/) directory contains examples for all GA Agentic API capabilities:

| Category | Example | Description |
|---|---|---|
| **Quickstart** | [`quickstart_api_key.py`](./examples/agenthub/quickstart_api_key.py) | API Key auth quickstart |
| | [`quickstart_oci_iam.py`](./examples/agenthub/quickstart_oci_iam.py) | OCI IAM auth quickstart |
| **Responses** | [`responses/create_response.py`](./examples/agenthub/responses/create_response.py) | Basic response |
| | [`responses/create_response_streaming.py`](./examples/agenthub/responses/create_response_streaming.py) | Streaming (delta text) |
| | [`responses/structured_output.py`](./examples/agenthub/responses/structured_output.py) | Structured output with Pydantic |
| | [`responses/choosing_models.py`](./examples/agenthub/responses/choosing_models.py) | Using different model providers |
| | [`responses/reasoning.py`](./examples/agenthub/responses/reasoning.py) | Reasoning effort and summary |
| **Multi-Modality** | [`responses/multimodal_image_base64.py`](./examples/agenthub/responses/multimodal_image_base64.py) | Image input (base64) |
| | [`responses/multimodal_image_url.py`](./examples/agenthub/responses/multimodal_image_url.py) | Image input (URL) |
| | [`responses/multimodal_file_id.py`](./examples/agenthub/responses/multimodal_file_id.py) | File input (File ID) |
| | [`responses/multimodal_file_url.py`](./examples/agenthub/responses/multimodal_file_url.py) | File input (URL) |
| **Tools** | [`tools/web_search.py`](./examples/agenthub/tools/web_search.py) | Web Search |
| | [`tools/file_search.py`](./examples/agenthub/tools/file_search.py) | File Search (Vector Store) |
| | [`tools/code_interpreter.py`](./examples/agenthub/tools/code_interpreter.py) | Code Interpreter |
| | [`tools/image_generation.py`](./examples/agenthub/tools/image_generation.py) | Image Generation |
| | [`tools/mcp_tool.py`](./examples/agenthub/tools/mcp_tool.py) | Remote MCP tool |
| | [`tools/function_calling.py`](./examples/agenthub/tools/function_calling.py) | Local function calling |
| | [`tools/multiple_tools.py`](./examples/agenthub/tools/multiple_tools.py) | Multiple tools in one request |
| **Conversation** | [`conversation/responses_chaining.py`](./examples/agenthub/conversation/responses_chaining.py) | Multi-turn via response chaining |
| | [`conversation/conversations_api.py`](./examples/agenthub/conversation/conversations_api.py) | Multi-turn via Conversations API |
| **Memory** | [`memory/long_term_memory.py`](./examples/agenthub/memory/long_term_memory.py) | Long-term memory across conversations |
| | [`memory/long_term_memory_access_policy.py`](./examples/agenthub/memory/long_term_memory_access_policy.py) | Memory access policy control |
| | [`memory/short_term_memory_optimization.py`](./examples/agenthub/memory/short_term_memory_optimization.py) | Short-term memory optimization |
| **Files** | [`files/files_api.py`](./examples/agenthub/files/files_api.py) | Files API (upload, list, retrieve, delete) |
| **Vector Stores** | [`vector_stores/vector_stores_api.py`](./examples/agenthub/vector_stores/vector_stores_api.py) | Vector Stores API (CRUD + search) |
| | [`vector_stores/vector_store_files_api.py`](./examples/agenthub/vector_stores/vector_store_files_api.py) | Vector Store Files API |
| | [`vector_stores/vector_store_file_batches_api.py`](./examples/agenthub/vector_stores/vector_store_file_batches_api.py) | Vector Store File Batches API |

---

## Examples (Legacy / Chat Completions)

### OCI Generative AI

Notes:

- **Cohere models do not support OpenAI-compatible API**

#### Using the OCI OpenAI Synchronous Client

```python
from oci_openai import OciOpenAI, OciSessionAuth

client = OciOpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
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
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
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
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.Client(
        auth=OciSessionAuth(profile_name="<profile name>"),
        headers={"CompartmentId": "<compartment ocid>"}
    ),
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

#### Using with langchain-openai

```python
from langchain_openai import ChatOpenAI
import httpx
from oci_openai import OciUserPrincipalAuth


llm = ChatOpenAI(
    model="<model name>",  # for example "xai.grok-4-fast-reasoning"
    api_key="OCI",
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    http_client=httpx.Client(
        auth=OciUserPrincipalAuth(profile_name="<profile name>"),
        headers={"CompartmentId": "<compartment ocid>"}
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
