import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
import os

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_or_create_collection(
    name="creator_knowledge",
    embedding_function=embedding_fn
)

def load_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text: str, chunk_size: int = 500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def add_pdf_to_knowledge_base(pdf_path: str, source_name: str):
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{source_name}_{i}"],
            metadatas=[{"source": source_name}]
        )
    
    return f"Added {len(chunks)} chunks from {source_name}"

def query_knowledge_base(question: str, n_results: int = 3):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    return results["documents"][0]

def rag_answer(question: str, groq_client, model: str):
    chunks = query_knowledge_base(question)
    context = "\n\n".join(chunks)
    
    prompt = f"""You are an expert Instagram growth strategist.
    
Use the following knowledge to answer the question:

{context}

Question: {question}

Give a clear, actionable answer based on the knowledge provided."""

    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content