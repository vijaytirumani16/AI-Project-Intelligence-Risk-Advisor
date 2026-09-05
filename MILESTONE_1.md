# Milestone 1

## 1. Study

### 1.1 RAG Architecture

RAG stands for Retrieval-Augmented Generation.

RAG combines two important components:

1. Retrieval – Relevant information is retrieved from a knowledge base.
2. Generation – A Large Language Model (LLM) uses the retrieved information to generate an answer.

### Basic RAG Architecture

User Question
↓
Convert Question into Embedding
↓
Vector Database Search
↓
Retrieve Relevant Document Chunks
↓
Send Context + Question to LLM
↓
Generate Final Answer

### RAG in This Project

In the AI Project Intelligence & Risk Advisor project, RAG will allow the system to:

- Read project documents.
- Retrieve relevant project information.
- Analyze risks and blockers.
- Identify action items.
- Answer project-related questions.

### Technologies Used

- Sentence Transformers – Generate embeddings.
- ChromaDB – Store and retrieve document embeddings.
- Gemini – Generate AI responses.


### 1.2 Multi-Agent Design Patterns

A multi-agent system consists of multiple AI agents, where each agent performs a specific task.

Instead of using one AI system for everything, different agents can have different responsibilities.

### Basic Multi-Agent Pattern

User Request
↓
Coordinator / Orchestrator
↓
Specialized Agents
↓
Combine Results
↓
Final Response

### Agent Roles Planned for This Project

The AI Project Intelligence & Risk Advisor can use specialized agents such as:

- Document Analysis Agent – Analyzes project documents.
- Risk Detection Agent – Identifies potential project risks.
- Blocker Detection Agent – Identifies project blockers.
- Action Item Agent – Extracts important action items.
- Delivery Forecast Agent – Identifies possible delivery delays.

### Benefits of Multi-Agent Systems

- Each agent has a specific responsibility.
- Complex tasks can be divided into smaller tasks.
- The system can be extended easily.
- Different agents can focus on different aspects of project intelligence.


### 1.3 Project Management Fundamentals

Project management involves planning, organizing, monitoring, and controlling project activities to achieve project goals.

Important project management concepts include:

- Project Scope – Defines the work and objectives of the project.
- Tasks – Individual activities that must be completed.
- Risks – Potential problems that may affect the project.
- Blockers – Issues that prevent project progress.
- Action Items – Specific tasks that need to be completed.
- Milestones – Important stages or checkpoints in a project.
- Deadlines – Target dates for completing tasks.

### Importance in This Project

The AI Project Intelligence & Risk Advisor will analyze project documents to identify important project information such as:

- Current project status.
- Project risks.
- Project blockers.
- Action items.
- Possible delivery delays.

These concepts help the system provide useful project intelligence and support project decision-making.






## 2. Design

### 2.1 System Architecture

The system architecture for the AI Project Intelligence & Risk Advisor is designed to process project documents and prepare them for intelligent retrieval and analysis.

### System Flow

Project Documents
(PDF, DOCX, CSV, TXT)
↓
Document Ingestion Module
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
Gemini AI / Future AI Agents
↓
Project Intelligence and Risk Analysis

### Architecture Components

- Document Ingestion Module – Reads PDF, DOCX, CSV, and TXT files.
- Document Processor – Processes multiple project documents.
- Text Chunking Module – Splits large documents into smaller chunks.
- Embedding Module – Converts text chunks into numerical embeddings.
- Vector Store – Stores embeddings and document information using ChromaDB.
- Retrieval Module – Retrieves relevant document information.
- AI Layer – Gemini and future specialized agents will analyze the retrieved information.

### 2.2 Agent Roles

The system is designed to support multiple specialized AI agents. Each agent will focus on a specific project management task.

### Planned Agent Roles

#### 1. Document Analysis Agent

Responsibilities:

- Analyze project documents.
- Extract important project information.
- Identify project status and relevant details.

#### 2. Risk Detection Agent

Responsibilities:

- Identify potential project risks.
- Analyze information that may affect the project timeline.
- Highlight high-risk areas.

#### 3. Blocker Detection Agent

Responsibilities:

- Identify issues that may prevent project progress.
- Detect dependencies or obstacles mentioned in project documents.

#### 4. Action Item Agent

Responsibilities:

- Extract action items from project documents.
- Identify tasks that require attention.

#### 5. Delivery Forecast Agent

Responsibilities:

- Analyze project progress.
- Identify possible delivery delays.
- Provide information about potential timeline risks.

### Agent Coordination

In the future system, a coordinator or orchestrator can manage the specialized agents and combine their results to generate overall project intelligence.

### 2.3 RAG Pipeline Design

The Retrieval-Augmented Generation (RAG) pipeline is designed to process project documents and make their information available for intelligent retrieval.

### Document Indexing Flow

Project Documents
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

### Retrieval Flow

User Question
↓
Question Embedding
↓
Vector Similarity Search
↓
Retrieve Relevant Document Chunks
↓
Provide Retrieved Context to AI
↓
Generate Intelligent Response

### RAG Components

- Document Ingestion – Reads supported project documents.
- Text Chunking – Splits documents into smaller pieces.
- Embedding Generation – Converts text into numerical vector representations.
- Vector Store – Stores document embeddings for similarity search.
- Retrieval – Finds the most relevant document chunks for a query.
- Generation – An AI model uses the retrieved context to generate a response.

### Implementation in This Project

The current Milestone 1 implementation includes document ingestion, chunking, embedding generation, and vector store indexing. The retrieval and AI response stages are prepared for further development.

### 2.4 Document Data Models

The system processes different types of project documents and represents their information in a structured format.

### Supported Document Model

Each uploaded project document can contain:

- File Name
- File Type
- Document Content

Example:

File Name: project_tasks.csv  
File Type: CSV  
Document Content: Task, Status, Risk information

### Document Chunk Model

After processing, each document is divided into smaller chunks.

Each chunk contains:

- Chunk Text
- Source File Name

Example:

{
    "text": "Testing Not Started High",
    "source": "project_tasks.csv"
}

### Embedding Model

Each text chunk is converted into a numerical embedding.

Example:

Document Chunk
↓
Sentence Transformer
↓
Numerical Vector

These embeddings allow the system to perform similarity-based document retrieval.

### Vector Store Model

The ChromaDB vector store contains:

- Document Chunk Text
- Embedding Vector
- Chunk ID
- Source Metadata

Example:

Chunk ID: chunk_0  
Document: Project document text  
Source: project_notes.txt  
Embedding: Numerical vector representation

This data model allows the system to identify both the document content and its original source.