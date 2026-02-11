import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
 
CHROMA_PATH = "chroma_db"

# We use Google's highly efficient embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def store_chunks(chunks: list[str], collection_name: str) -> Chroma:
    """
    Converts text chunks into embeddings and stores them in a ChromaDB collection.
    Each video/upload gets its own collection name (usually the file hash).
    """
    print(f"Storing {len(chunks)} chunks in ChromaDB collection: {collection_name}...")
    
    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_PATH
    )
    
    return vector_db

def get_vector_store(collection_name: str) -> Chroma:
    """Retrieves an existing ChromaDB collection for querying."""
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )