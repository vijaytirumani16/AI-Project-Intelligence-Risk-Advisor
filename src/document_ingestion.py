from pathlib import Path
import pandas as pd
from pypdf import PdfReader
from docx import Document


def read_txt(file_path):
    """Read text from a TXT file."""
    return Path(file_path).read_text(encoding="utf-8")


def read_pdf(file_path):
    """Read text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"

    return text


def read_docx(file_path):
    """Read text from a DOCX file."""
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def read_csv(file_path):
    """Read data from a CSV file as text."""
    dataframe = pd.read_csv(file_path)

    return dataframe.to_string(index=False)


def read_document(file_path):
    """Read a document based on its file type."""

    file_extension = Path(file_path).suffix.lower()

    if file_extension == ".txt":
        return read_txt(file_path)

    elif file_extension == ".pdf":
        return read_pdf(file_path)

    elif file_extension == ".docx":
        return read_docx(file_path)

    elif file_extension == ".csv":
        return read_csv(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {file_extension}"
        )