# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples.common import oci_openai_client

deleted_response = oci_openai_client.responses.delete(
    response_id="resp_sjc_qw1r6si1yt9vu959lrajoid2m5jflwnhh0jammcchdh9ibpg"
)
print(deleted_response)
