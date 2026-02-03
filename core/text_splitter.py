# Decoupage des documents en chunks

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def create_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter

def split_documents(documents: list) -> list:
    text_splitter = create_text_splitter()
    chunks = text_splitter.split_documents(documents)

    print(f"{len(documents)} documents découpés en {len(chunks)} chunks")
    return chunks