# Copyright (c) 2025 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Files API examples - upload, list, retrieve, retrieve content, and delete files."""

from pathlib import Path

from examples.agenthub.common import kix_client

# List files in the project
files_list = kix_client.files.list(order="asc")
for file in files_list.data:
    print(f"{file.id:<45} {file.status:<10} {file.filename}")

#  assuming the file "2024ltr.pdf" is in the same directory as this script
pdf_file_path = Path(__file__).parent / "2024ltr.pdf"

# Upload a file
with open(pdf_file_path, "rb") as f:
    file = kix_client.files.create(
        file=f,
        purpose="user_data",
    )
    print("Uploaded file:", file)

# Retrieve file metadata
file = kix_client.files.retrieve(file_id="file-kix-5d04dec2-b59d-4330-84c7-6c0a804c4996")
print("\nRetrieved file:", file)

# Retrieve file content
content = kix_client.files.content(file_id="file-kix-5d04dec2-b59d-4330-84c7-6c0a804c4996")
print("\nFile content:", content)

# Delete file
delete_result = kix_client.files.delete(file_id="file-kix-8107c258-e916-4af8-a40b-6a04fa1c4bdd")
print("\nDelete result:", delete_result)
