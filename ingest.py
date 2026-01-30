import sys
import os

# -------------------------------
# Ensure venv is active
# -------------------------------
if ".venv" not in sys.executable:
    raise RuntimeError("❌ Virtual environment not activated")

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

VECTOR_DB_DIR = "faiss_index"

# -------------------------------
# Embeddings OBJECT (IMPORTANT)
# -------------------------------
class LocalEmbeddings:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()


embeddings = LocalEmbeddings()
documents = []

# -------------------------------
# Local file paths
# -------------------------------
FILE_PATHS = [
    r"C:\Users\LuckySingh\IVF_chatbot\data\A15337.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\IJCRT2507656.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\ijerph-20-03952.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\IJRAR1DOP016.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\JETIR2509354.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\pone.0286518.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\s13048-025-01692-5.pdf",
    r"C:\Users\LuckySingh\IVF_chatbot\data\IVF_and_Fertility_Treatment_Options.docx",
    r"C:\Users\LuckySingh\IVF_chatbot\data\IVF_and_IVF_Clinic_Working_Detailed.docx",
]

for path in FILE_PATHS:
    print(f"Loading file: {path}")

    if not os.path.exists(path):
        print(f"⚠️ Missing file, skipped: {path}")
        continue

    if path.lower().endswith(".pdf"):
        documents.extend(PyPDFLoader(path).load())

    elif path.lower().endswith(".docx"):
        documents.extend(UnstructuredWordDocumentLoader(path).load())

# -------------------------------
# Trusted IVF websites
# -------------------------------
WEB_URLS = [
    "https://www.who.int/news-room/fact-sheets/detail/infertility",
    "https://www.nhs.uk/conditions/ivf/",
    "https://www.mayoclinic.org/tests-procedures/in-vitro-fertilization/about/pac-20384716",
]

for url in WEB_URLS:
    print(f"Loading web: {url}")
    documents.extend(WebBaseLoader(url).load())

print(f"✅ Loaded documents: {len(documents)}")

# -------------------------------
# Chunking
# -------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=80
)

chunks = splitter.split_documents(documents)

# -------------------------------
# FAISS (THIS LINE WAS THE BUG)
# -------------------------------
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings   # ✅ OBJECT, not function
)

vectorstore.save_local(VECTOR_DB_DIR)

print("🎉 FAISS index created successfully")
