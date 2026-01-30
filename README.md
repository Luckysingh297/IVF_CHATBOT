# IVF_CHATBOT  
A Retrieval-Augmented Generation (RAG) based IVF knowledge assistant built using **Streamlit + LangChain + FAISS + SentenceTransformers**.  
This project helps users ask IVF-related questions and get responses grounded in trusted documents and web sources.

---

## Project Overview
**IVF_CHATBOT** is an AI-powered assistant designed to support users with IVF-related information by combining:
- Document ingestion (PDF/DOCX + web pages)
- Text chunking
- Vector search using FAISS
- Context-aware answer generation via RAG pipeline
- A clean Streamlit chat-style UI

✅ Goal: Provide **accurate, document-grounded answers** instead of random generic responses.

---

##  Key Features
✅ **RAG Pipeline (Retrieval-Augmented Generation)**  
✅ **FAISS Vector Database** for fast semantic search  
✅ **Local Embeddings** using `all-MiniLM-L6-v2`  
✅ **Supports multiple data sources**:
- PDF documents
- DOCX documents
- Web links

✅ **Streamlit Chat UI** with session handling  
✅ Clean project structure + GitHub ready

---

## 🛠 Tech Stack
- **Python**
- **Streamlit** (UI)
- **LangChain**
- **FAISS**
- **SentenceTransformers**
- **Document Loaders** (PDF, DOCX, Web)