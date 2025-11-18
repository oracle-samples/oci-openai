from rich import print

from examples.common import oci_openai_client


def main():
    model = "openai.gpt-4.1"

    tools = [
        {
            "type": "web_search",
        }
    ]

    # First Request
    response1 = oci_openai_client.responses.create(
        model=model, input="please tell me today break news", tools=tools, store=False
    )
    print(response1.output)


if __name__ == "__main__":
    main()
