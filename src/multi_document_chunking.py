import os

from document_processor import process_documents
from chunking import chunk_text


def process_and_chunk_documents(data_folder):

    documents = process_documents(data_folder)

    all_chunks = []

    file_names = os.listdir(data_folder)

    supported_files = [
        file_name
        for file_name in file_names
        if file_name.endswith(
            (".txt", ".docx", ".pdf", ".csv")
        )
    ]

    for document, file_name in zip(
        documents,
        supported_files
    ):

        chunks = chunk_text(document)

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "source": file_name
            })

    return all_chunks