# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client


def main():
    model = "openai.gpt-4.1"

    # First Request
    response1 = oci_openai_client.responses.create(
        model=model,
        input="Explain what OKRs are in 2 sentences.",
        previous_response_id=None,  # root of the history
    )
    print(response1.output)

    # Second Request with previousResponseId of first request
    response2 = oci_openai_client.responses.create(
        model=model,
        input="Based on that, list 3 common pitfalls to avoid.",
        previous_response_id=response1.id,  # new branch from response1
    )
    print(response2.output)

    # Second Request with previousResponseId of third request
    response3 = oci_openai_client.responses.create(
        model=model,
        input="Expand bit more on OKRs in a paragraph summary.",
        previous_response_id=response1.id,  # new branch from response1
    )
    print(response3.output)


if __name__ == "__main__":
    main()
