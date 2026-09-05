import os

from document_ingestion import read_txt
from document_ingestion import read_docx
from document_ingestion import read_pdf
from document_ingestion import read_csv


def process_documents(data_folder):

    documents = []

    for file_name in os.listdir(data_folder):

        file_path = os.path.join(data_folder, file_name)

        if file_name.endswith(".txt"):

            content = read_txt(file_path)
            documents.append(content)

        elif file_name.endswith(".docx"):

            content = read_docx(file_path)
            documents.append(content)

        elif file_name.endswith(".pdf"):

            content = read_pdf(file_path)
            documents.append(content)

        elif file_name.endswith(".csv"):

            content = read_csv(file_path)
            documents.append(content)

    return documents