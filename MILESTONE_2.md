# Milestone 2 – Multi-Agent Project Intelligence

## 1. Milestone Objective

The objective of Milestone 2 is to implement a multi-agent project
intelligence pipeline that analyzes uploaded project documents and
extracts project scope, identifies risks and delivery challenges,
and detects blockers and action items.

The agents use the existing RAG pipeline and project knowledge base
to ground their analysis in the uploaded project documents.

---

## 2. Milestone 2 Requirements

Milestone 2 consists of the following components:

1. Scope and Deliverable Extraction Agent
2. Risk Detection and Delivery Forecasting Agent
3. Blocker and Action Item Identification Agent
4. Validation using sample project documents across different formats

---

## 3. Scope and Deliverable Extraction Agent

### Purpose

The Scope and Deliverable Extraction Agent analyzes project documents
and extracts important project scope information.

### Information Extracted

- Project Goals
- Deliverables
- Milestones
- Timeline
- Responsibilities

### Implementation

The agent is implemented in:

`src/scope_agent.py`

It uses the existing RAG function:

`ask_question()`

The RAG pipeline retrieves relevant project information from the
ChromaDB vector store before sending the information to the Gemini
language model.

### Output Behavior

The agent is instructed to use only information available in the
uploaded project documents.

When information is not available, the agent reports:

"Not specified in the documents."

This prevents the system from inventing project information.

---

## 4. Risk Detection and Delivery Forecasting Agent

### Purpose

The Risk Detection and Delivery Forecasting Agent analyzes project
documents to identify risks that may affect project progress and
delivery.

### Information Extracted

- Schedule Risks
- Dependency Gaps
- Delivery Challenges
- Possible Delivery Delays
- Risk Priority when supported by the documents

### Implementation

The agent is implemented in:

`src/risk_delivery_agent.py`

The agent uses the existing RAG pipeline to retrieve relevant project
information and generate a document-grounded analysis.

### Identified Project Risks

During validation, the agent identified potential delays caused by:

- Incomplete document processing
- Delay in completing the RAG pipeline

The agent correctly reported that dependency gaps and risk priorities
were not specified when sufficient information was not available.

---

## 5. Blocker and Action Item Identification Agent

### Purpose

The Blocker and Action Item Identification Agent identifies unresolved
project issues, blockers, pending decisions, and actions that need to
be completed.

### Information Extracted

- Pending Decisions
- Unresolved Issues
- Blockers
- Action Items
- Assigned Responsibilities

### Implementation

The agent is implemented in:

`src/blocker_action_agent.py`

The agent uses the existing RAG pipeline and Gemini model to analyze
the project information retrieved from the vector database.

### Identified Action Items

During validation, the agent identified the following pending actions:

- Complete testing of all document ingestion modules.
- Complete the document ingestion module and test all supported file types.
- Test PDF document ingestion successfully.

The agent correctly reported that pending decisions, active blockers,
and assigned responsibilities were not specified in the available
project documents.

---

## 6. Multi-Agent Architecture

The Milestone 2 architecture extends the RAG pipeline implemented
during Milestone 1.

```text
Project Documents
(PDF / DOCX / CSV / TXT)
          |
          v
Document Ingestion
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
     RAG Retrieval
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
Multi-Agent Project Intelligence


---

## Validation

The Milestone 2 agents were validated using the existing project
knowledge base containing sample documents in multiple formats:

- TXT
- DOCX
- PDF
- CSV

The combined validation test is implemented in:

`src/test_milestone_2.py`

### Validation Results

- Scope and Deliverable Extraction Agent — **PASS**
- Risk Detection and Delivery Forecasting Agent — **PASS**
- Blocker and Action Item Identification Agent — **PASS**

All three agents executed successfully and generated
document-grounded project intelligence.

### Known Limitation

Some information such as detailed milestone dates, assigned
responsibilities, explicit task dependencies, and pending decisions
is not available in the current sample documents.

The agents therefore report such information as:

`Not specified in the documents.`

This prevents unsupported information from being generated.

---

## Milestone 2 Completion

Milestone 2 multi-agent functionality has been implemented and
validated successfully.

Completed components:

- Scope and Deliverable Extraction Agent
- Risk Detection and Delivery Forecasting Agent
- Blocker and Action Item Identification Agent
- Multi-agent validation using project document data