# AI Project Intelligence & Risk Advisor

## Project Overview

AI Project Intelligence & Risk Advisor is an AI-based project management system designed to analyze project documents and identify useful project information such as risks, blockers, action items, and possible delivery delays.

## Milestone 1

Milestone 1 focuses on building the foundation of the project.

### Completed Features

- Document ingestion for TXT files
- Document ingestion for PDF files
- Document ingestion for DOCX files
- Document ingestion for CSV files
- Multi-document processing
- Text chunking
- Source information preservation
- Embedding generation using Sentence Transformers
- Vector store indexing using ChromaDB

## RAG Pipeline

```text
Project Documents
(PDF, DOCX, CSV, TXT)
        ↓
Document Ingestion
        ↓
Document Processing
        ↓
Text Chunking
        ↓
Embedding Generation
        ↓
ChromaDB Vector Store
        ↓
Document Retrieval
        ↓
Future AI Analysis