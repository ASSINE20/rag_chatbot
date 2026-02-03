# Chargement des documents PDF

import tempfile
import os
from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader


def load_pdf(file_path: str) -> list:
    """
    Charge un seul fichier PDF

    Args:
        file_path: chemin du fichier PDF

    Returns:
        Liste de documents (pages)
    """
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return documents

def load_upploaded_files(uploaded_files) -> list:
    """
    Charge plusieurs fichiers uploades via Streamlit

    Args:
        uploaded_files: Fichiers uploades depuis st.file_uploader

    Returns:
        Liste de tous les documents
    """

    all_docs = []

    # Dossier temporaire pour stocker les fichiers
    temp_dir = tempfile.TemporaryDirectory()

    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)

        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())

        # Charger le PDF
        docs = load_pdf(temp_filepath)
        all_docs.extend(docs)

        print(f"Chargé: {file.name} ({len(docs)} pages)")
        return all_docs