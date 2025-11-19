# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client


def main():
    model = "openai.gpt-4.1"

    conversation = oci_openai_client.conversations.create(metadata={"topic": "demo"})
    print(conversation)

    response = oci_openai_client.responses.create(
        model=model, input="Explain what OKRs are in 2 sentences.", conversation=conversation.id
    )
    print(response.output)

    response = oci_openai_client.responses.create(
        model=model, input="what was my previous question from user?", conversation=conversation.id
    )
    print(response.output)

    response = oci_openai_client.responses.create(
        model=model,
        input="Based on that, list 3 common pitfalls to avoid.",
        conversation=conversation.id,
    )
    print(response.output)


if __name__ == "__main__":
    main()
