# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Vector Stores API examples - create, list, retrieve, update, search, and delete."""

from examples.agenthub.common import oci_openai_client

# Create a vector store
vector_store = oci_openai_client.vector_stores.create(
    name="demo-vector-store",
    description="Demo vector store for testing",
    expires_after={
        "anchor": "last_active_at",
        "days": 30,
    },
    metadata={
        "topic": "oci",
    },
)
print("Created vector store:", vector_store.id)

# List vector stores
list_result = oci_openai_client.vector_stores.list(limit=20, order="desc")
print("\nVector stores:", list_result)

# Retrieve vector store
retrieve_result = oci_openai_client.vector_stores.retrieve(
    vector_store_id=vector_store.id,
)
print("\nRetrieved:", retrieve_result)

# Update vector store
update_result = oci_openai_client.vector_stores.update(
    vector_store_id=vector_store.id,
    name="Updated Demo Vector Store",
    metadata={"category": "history", "period": "medieval"},
)
print("\nUpdated:", update_result)

# Search vector store (requires files to be added first)
# search_results = oci_openai_client.vector_stores.search(
#     vector_store_id=vector_store.id,
#     query="What are OCI GPU shapes?",
#     max_num_results=10,
# )
# print("\nSearch results:", search_results)

# Delete vector store
delete_result = oci_openai_client.vector_stores.delete(
    vector_store_id=vector_store.id,
)
print("\nDeleted:", delete_result)
