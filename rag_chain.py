import ollama
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

# -----------------------------
# Embeddings (MUST inherit)
# -----------------------------
class LocalEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode(text).tolist()

vectorstore = FAISS.load_local(
    "faiss_index",
    LocalEmbeddings(),
    allow_dangerous_deserialization=True
)

# -----------------------------
# RAG FUNCTION
# -----------------------------
def ask_question(question: str, mode: str) -> str:
    docs = vectorstore.similarity_search(question, k=4)

    if not docs:
        return "The provided sources do not specify this information."

    context = "\n\n".join(d.page_content for d in docs)

    style = {
        "Short": "Answer in 2–3 short sentences only.",
        "Detailed": "Answer in a clear, structured explanation.",
        "Bullet": "Answer strictly in bullet points."
    }[mode]

    prompt = f"""
You are an IVF medical assistant.

RULES:
- Use ONLY the context
- No diagnosis or treatment advice
- Follow style strictly
- Do NOT mention sources
- Be medically accurate

STYLE:
{style}

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.generate(
        model="mistral",
        prompt=prompt,
        options={
            "temperature": 0.7,
            "top_p": 0.9
        }
    )

    return response["response"].strip()
