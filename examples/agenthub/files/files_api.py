# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Files API examples - upload, list, retrieve, retrieve content, and delete files."""

from examples.agenthub.common import oci_openai_client

# Upload a file
file_path = "./demo_file.pdf"
with open(file_path, "rb") as f:
    file = oci_openai_client.files.create(
        file=f,
        purpose="user_data",
    )
    print("Uploaded file:", file)

# List files
files_list = oci_openai_client.files.list(order="asc")
print("\nFiles list:", files_list)

# Retrieve file metadata
file = oci_openai_client.files.retrieve(file_id=file.id)
print("\nRetrieved file:", file)

# Retrieve file content
content = oci_openai_client.files.content(file_id=file.id)
print("\nFile content length:", len(content.content))

# Delete file
delete_result = oci_openai_client.files.delete(file_id=file.id)
print("\nDelete result:", delete_result)
