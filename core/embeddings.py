# Creer les embeddings et gerer ChromaDB

import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config.settings import CHROMA_PATH, RETRIEVER_K

def create_embeddings_model():
    embeddings_model = OpenAIEmbeddings()
    return embeddings_model

def create_vector_store(chunks: list):
    # Modele d'embeddings
    embeddings_model = create_embeddings_model()

    # Client ChromaDB persistant
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Creer la base vectorielle
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding =embeddings_model,
        client=client,
        collection_name="document_collection"
    )
    print(f"Base vectorielle créée avec {len(chunks)} chunks")
    return vector_store

def get_retriever(vector_store):
    """
    Creer un retriever a partir de la base vectorielle

    Args:
        vector_store: Chroma vector store
    Returns:
        Retriever configuré
    """
    retriever = vector_store.as_retriever(
        search_kwargs={"k": RETRIEVER_K}
    )
    return retriever

def create_retriver_from_documents(chunks: list):
    """
    Fonction combinée: crée la base vectorielle et retourne le retriever

    Args:
        chunks: Liste de chunks de documents
    Returns:
        Retriever pret a etre utilise
    """
    vector_store = create_vector_store(chunks)
    retriever = get_retriever(vector_store)
    return retriever