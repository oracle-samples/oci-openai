# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client


def main():
    model = "openai.gpt-4.1"
    tools = [
        {
            "type": "mcp",
            "server_label": "deepwiki",
            "require_approval": "never",
            #  "authorization": "key",
            "server_url": "https://mcp.deepwiki.com/mcp",
        }
    ]

    # First Request
    response1 = oci_openai_client.responses.create(
        model=model, input="please tell me structure about facebook/react", tools=tools, store=False
    )
    print(response1.output)


if __name__ == "__main__":
    main()
