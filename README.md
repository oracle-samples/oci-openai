# oci-openai

[![PyPI - Version](https://img.shields.io/pypi/v/oci-openai.svg)](https://pypi.org/project/oci-openai)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oci-openai.svg)](https://pypi.org/project/oci-openai)

OCI-OpenAI is a client library maintained by the Oracle Cloud Infrastructure (OCI) [Generative AI Service](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm) team.
This package simplifies integration between OpenAI’s Python SDK and Oracle Cloud Infrastructure (OCI) GenAI service by providing robust authentication and authorization utilities.
Developers can seamlessly connect to Oracle Generative AI services using OCI credentials, ensuring secure and compliant access while leveraging industry best practices.

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install oci-openai
```

## Examples

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

## Contributing

This project welcomes contributions from the community. Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md)

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process

## License

Copyright (c) 2025 Oracle and/or its affiliates.

Released under the Universal Permissive License v1.0 as shown at
<https://oss.oracle.com/licenses/upl/>