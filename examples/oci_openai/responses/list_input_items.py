from rich import print

from examples.common import oci_openai_client

response = oci_openai_client.responses.input_items.list(
    "resp_sjc_qw1r6si1yt9vu959lrajoid2m5jflwnhh0jammcchdh9ibpg"
)
print(response)
