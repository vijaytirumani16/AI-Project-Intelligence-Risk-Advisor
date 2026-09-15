# AI Project Intelligence & Risk Advisor

## Project Overview

AI Project Intelligence & Risk Advisor is an AI-based project management system designed to analyze project documents and provide useful project intelligence such as project scope, deliverables, risks, blockers, action items, and possible delivery delays.

The system accepts project documents in multiple formats and uses a Retrieval-Augmented Generation (RAG) pipeline to provide document-grounded analysis.

---

# Milestone 1

Milestone 1 focuses on building the document processing and RAG foundation of the project.

## Completed Features

- Document ingestion for TXT files
- Document ingestion for PDF files
- Document ingestion for DOCX files
- Document ingestion for CSV files
- Multi-document processing
- Text chunking
- Source information preservation
- Embedding generation using Sentence Transformers
- Vector store indexing using ChromaDB
- Document retrieval using the vector store

---

# Milestone 2

Milestone 2 focuses on implementing a multi-agent project intelligence pipeline using the RAG foundation developed in Milestone 1.

## Completed Features

### 1. Scope and Deliverable Extraction Agent

The Scope and Deliverable Extraction Agent identifies:

- Project goals
- Deliverables
- Milestones
- Timeline information
- Responsibilities

Implementation:

`src/scope_agent.py`

---

### 2. Risk Detection and Delivery Forecasting Agent

The Risk Detection and Delivery Forecasting Agent identifies:

- Schedule risks
- Dependency gaps
- Delivery challenges
- Possible delivery delays
- Risk priority when supported by the documents

Implementation:

`src/risk_delivery_agent.py`

---

### 3. Blocker and Action Item Identification Agent

The Blocker and Action Item Identification Agent identifies:

- Pending decisions
- Unresolved issues
- Blockers
- Action items
- Assigned responsibilities when explicitly available

Implementation:

`src/blocker_action_agent.py`

---

## Multi-Agent Architecture

```text
Project Documents
(PDF, DOCX, CSV, TXT)
        |
        v
Document Ingestion
        |
        v
Document Processing
        |
        v
Text Chunking
        |
        v
Embedding Generation
        |
        v
ChromaDB Vector Store
        |
        v
Document Retrieval
        |
        v
RAG Pipeline
        |
   +----+----+
   |    |    |
   v    v    v
Scope  Risk  Blocker
Agent  Agent  Agent
   |    |    |
   +----+----+
        |
        v
Project Intelligence