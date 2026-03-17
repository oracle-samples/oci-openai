# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples.agenthub.common import kix_client, kix_cp_client
import time

"""Vector Store Search example."""

VS_COMPARTMENT_ID = "ocid1.tenancy.oc1..aaaaaaaasz6cicsgfbqh6tj3xahi4ozoescfz36bjm3kucc7lotk2oqep47q"

# Upload a file using the Files API
file = kix_client.files.create(
    file=open("/Users/jgyang/Downloads/2312.10997v1.pdf", "rb"),
    purpose="user_data",
)
print("Uploaded file:", file.id)

# Create a vector store
vector_store = kix_cp_client.vector_stores.create(
    name="OCI Support FAQ Vector Store",
    description="My vector store for supporting customer queries",
    expires_after={
        "anchor": "last_active_at",
        "days": 30,
    },
    extra_headers={
      "opc-compartment-id": VS_COMPARTMENT_ID,
    }
)
print("Created vector store:", vector_store.id)

# Wait for vector store resource to be in the "completed" state
while True:
    vector_store = kix_cp_client.vector_stores.retrieve(
        vector_store_id=vector_store.id,
        extra_headers={
            "opc-compartment-id": VS_COMPARTMENT_ID,
        }
    )
    print("Vector store status:", vector_store.status)
    if vector_store.status == "completed":
        break
    else:
        time.sleep(5)

# Wait a few more seconds after completed state for the vector store to be fully activated
time.sleep(10)

# Add a file to a vector store using the Vector Store Files API
create_result = kix_client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id,
    attributes={"category": "history"},
)
print("Created vector store file:", create_result)

while True:
    file_status = kix_client.vector_stores.files.retrieve(
        vector_store_id=vector_store.id,
        file_id=file.id,
    )
    print("Vector store file status:", file_status.status)
    if file_status.status == "completed":
        break
    else:
        time.sleep(3)

# Now the vector store file is indexed, we can search the vector store by a query term
search_results_page = kix_client.vector_stores.search(
    vector_store_id=vector_store.id,
    query="Retrieval-Augmented Generation",
    max_num_results=10,
)
print("\nSearch results page:", search_results_page)

if search_results_page.data:
    for page_data in search_results_page.data:
        print("\nSearch results page data:", page_data)
else:
    print("\nNo search results found")