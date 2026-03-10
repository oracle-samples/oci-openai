# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from examples.agenthub.common import cp_client

"""Vector Stores API examples - create, list, retrieve, update, search, and delete."""

VS_COMPARTMENT_ID = "ocid1.tenancy.oc1..aaaaaaaasz6cicsgfbqh6tj3xahi4ozoescfz36bjm3kucc7lotk2oqep47q"

# Create a vector store
vector_store = cp_client.vector_stores.create(
    name="OCI Support FAQ Vector Store",
    description="My vector store for supporting customer queries",
    expires_after={
        "anchor": "last_active_at",
        "days": 30,
    },
    metadata={
        "topic": "oci",
    },
    extra_headers={
      "opc-compartment-id": VS_COMPARTMENT_ID,
    }
)
print("Created vector store:", vector_store.id)

# List vector stores
list_result = cp_client.vector_stores.list(
  limit=20,
  order="desc",
  extra_headers={ "opc-compartment-id": VS_COMPARTMENT_ID }
)
print("\nVector stores:", list_result)

# Retrieve vector store
retrieve_result = cp_client.vector_stores.retrieve(
    vector_store_id=vector_store.id,
    extra_headers={ "opc-compartment-id": VS_COMPARTMENT_ID }
)
print("\nRetrieved:", retrieve_result)

# Update vector store
update_result = cp_client.vector_stores.update(
    vector_store_id=vector_store.id,
    name="Updated Demo Vector Store",
    metadata={"category": "history", "period": "medieval"},
    extra_headers={ "opc-compartment-id": VS_COMPARTMENT_ID }
)
print("\nUpdated:", update_result)

# Delete vector store
delete_result = cp_client.vector_stores.delete(
    vector_store_id=vector_store.id,
    extra_headers={ "opc-compartment-id": VS_COMPARTMENT_ID }
)
print("\nDeleted:", delete_result)