# RAG SQL Injection

A Retrieval-Augmented Generation (RAG) project focused on combining Python, PostgreSQL, vector embeddings, SQL, and a web interface.

The project was created to explore how a RAG system can be built by combining document processing, vector retrieval, and a database.

> **Note:** The project currently does not include an integrated LLM. The retrieval and database components are being developed independently due to the cost of running or accessing an external LLM.

---

## Technologies

### Python

Python was selected as the primary language for the RAG and backend components.

It provides a strong ecosystem for:

- Data processing
- Natural language processing
- Embeddings
- API development
- Database integration

The Python layer is responsible for the main RAG pipeline and communication between the different components of the application.

### FastAPI

FastAPI is used as the backend framework.

It provides the API layer that connects the web interface with the Python application.

FastAPI was selected because it is lightweight, modern, and well suited for Python-based APIs.

### PostgreSQL

PostgreSQL was selected as the database system for the project.

The PostgreSQL database was designed and implemented by me and is responsible for storing and managing the application's data and vector information.

PostgreSQL was chosen because of:

- Strong relational database capabilities
- Powerful SQL support
- Reliability
- Extensibility
- Excellent Python integration
- Support for vector-based applications

### SQL

I personally designed and implemented the SQL portion of the project.

This includes the database logic and queries used to:

- Store data
- Retrieve information
- Manage records
- Interact with PostgreSQL
- Support the retrieval process

Working directly with SQL was an important part of the project because the database is a fundamental component of the RAG system.

### HTML

The web interface was implemented using HTML.

The purpose of the interface is to provide a simple way to interact with the application through a browser.

The HTML layer communicates with the backend instead of directly interacting with the database.

### Vector Embeddings

Vector embeddings are used to represent information in a numerical format that can be used for semantic retrieval.

The embeddings allow the system to find information that is semantically relevant to a user's query.

---

## Current RAG Pipeline

The current project focuses on the retrieval portion of the RAG architecture:

```text
Input Data
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
PostgreSQL
    │
    ▼
Vector Retrieval
    │
    ▼
Relevant Context
