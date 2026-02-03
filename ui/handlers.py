# Handlers pour gerer le streaming et l'affichage des sources

import streamlit as st
import pandas as pd
from langchain_core.callbacks.base import BaseCallbackHandler


# Gestion de l'affichage en temps reel des tokens generes par le LLM
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Gestion de l'affichage des sources documentaires apres la reponse
class PostMessageHandler(BaseCallbackHandler):
    def __init__(self):
        """Initialiser le handler"""
        BaseCallbackHandler.__init__(self)
        self.sources = []

    def on_retriever_end(self, documents, *, run_id, parent_run_id, **kwargs):
        source_ids = []
        for doc in documents:
            # Extraction des metadonnees
            metadata = {
                "source": doc.metadata.get("source", "Inconnu"),
                "page": doc.metadata.get("page", "N/A"),
                "extrait": doc.page_content[:200] + "..."
            }
            # Eviter les doublons
            idx = (metadata["source"], metadata["page"])
            if idx not in source_ids:
                source_ids.append(idx)
                self.sources.append(metadata)

    def on_llm_new_token(self, response, *, run_id, parent_run_id, **kwargs):
        if len(self.sources) > 0:
            st.markdown("---")
            st.markdown("** Sources utilisées:**")
            st.dataframe(
                data=pd.DataFrame(self.sources[:3]),
                width=1000,
                hide_index=True
            )