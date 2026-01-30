# IVF Chatbot - AI Agent Instructions

## Project Overview
This is a Retrieval-Augmented Generation (RAG) chatbot for IVF (In Vitro Fertilization) information. The system ingests educational PDF documents, creates vector embeddings, and stores them in a Chroma database for semantic search and question answering.

## Architecture
- **Data Ingestion**: `ingest.py` processes PDFs from `data/` directory
- **Vector Storage**: Chroma database in `chroma_db/` directory
- **Chatbot Interface**: `app.py` (currently empty, implement the chat interface here)
- **Data Source**: IVF educational materials in PDF format

## Key Components
- **Document Loading**: Uses LangChain's PyPDFLoader for PDF processing
- **Text Splitting**: RecursiveCharacterTextSplitter with 500 char chunks, 80 char overlap
- **Embeddings**: HuggingFace sentence-transformers/all-MiniLM-L6-v2 model
- **Metadata**: All chunks tagged with `domain: "IVF"` and `type: "educational"`

## Development Workflow
1. **Setup Environment**: Activate virtual environment with `.venv\Scripts\activate`
2. **Install Dependencies**: `pip install langchain langchain-community chromadb sentence-transformers`
3. **Ingest Data**: Run `python ingest.py` to build knowledge base from PDFs in `data/`
4. **Run Chatbot**: Implement and run `app.py` for the chat interface

## Code Patterns
- **File Structure**: Keep data processing in separate scripts (ingest.py), main app in app.py
- **Metadata Convention**: Add domain and type metadata to all document chunks
- **Embedding Model**: Use consistent sentence-transformers model for both ingestion and querying
- **Vector DB Path**: Store Chroma DB in `chroma_db/` directory

## Dependencies
Core packages: langchain, chromadb, sentence-transformers, pypdf (via PyPDFLoader)

## Common Tasks
- **Add New Documents**: Place PDFs in `data/` and re-run `ingest.py`
- **Query Database**: Load existing Chroma DB from `chroma_db/` for chat functionality
- **Debug Embeddings**: Check chunk metadata and similarity search results

## File References
- [ingest.py](ingest.py): Data ingestion pipeline
- [data/](data/): Source documents directory
- `chroma_db/`: Vector database storage (created by ingest.py)</content>
<parameter name="filePath">c:\Users\LuckySingh\IVF_chatbot\.github\copilot-instructions.md