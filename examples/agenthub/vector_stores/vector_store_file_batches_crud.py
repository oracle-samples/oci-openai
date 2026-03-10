# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Vector Store File Batches API examples - batch add files to a vector store."""

from examples.agenthub.common import client

VECTOR_STORE_ID = "<your-vector-store-id>"

# Create a batch with file IDs and shared attributes
batch_result = client.vector_stores.file_batches.create(
    vector_store_id=VECTOR_STORE_ID,
    file_ids=["file_id_1", "file_id_2", "file_id_3"],
    attributes={"category": "history"},
)
print("Created batch:", batch_result)

# Retrieve batch status
retrieve_result = client.vector_stores.file_batches.retrieve(
    vector_store_id=VECTOR_STORE_ID,
    batch_id=batch_result.id,
)
print("\nBatch status:", retrieve_result)

# List files in a batch
list_result = client.vector_stores.file_batches.list_files(
    vector_store_id=VECTOR_STORE_ID,
    batch_id=batch_result.id,
)
print("\nBatch files:", list_result)