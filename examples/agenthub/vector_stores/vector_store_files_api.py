# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Vector Store Files API examples - add, list, retrieve, update, and delete files."""

from examples.agenthub.common import client

VECTOR_STORE_ID = "<your-vector-store-id>"
FILE_ID = "<your-file-id>"

# Add a file to a vector store
create_result = client.vector_stores.files.create(
    vector_store_id=VECTOR_STORE_ID,
    file_id=FILE_ID,
    attributes={"category": "history"},
)
print("Created vector store file:", create_result)

# List vector store files
list_result = client.vector_stores.files.list(
    vector_store_id=VECTOR_STORE_ID,
)
print("\nFiles:", list_result)

# Retrieve vector store file
retrieve_result = client.vector_stores.files.retrieve(
    vector_store_id=VECTOR_STORE_ID,
    file_id=FILE_ID,
)
print("\nRetrieved:", retrieve_result)

# Update vector store file attributes
update_result = client.vector_stores.files.update(
    vector_store_id=VECTOR_STORE_ID,
    file_id=FILE_ID,
    attributes={"category": "history", "period": "medieval"},
)
print("\nUpdated:", update_result)

# Delete vector store file (removes parsed content, not the original file)
delete_result = client.vector_stores.files.delete(
    vector_store_id=VECTOR_STORE_ID,
    file_id=FILE_ID,
)
print("\nDeleted:", delete_result)
