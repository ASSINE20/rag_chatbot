# Application Streamlit - Chatbot RAG pour documents PDF

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from config.settings import (
setup_environment, AVAILABLE_MODELS, DEFAULT_TEMPERATURE, DEFAULT_MODEL)

from config.settings import setup_environment
from core.document_loader import load_upploaded_files
from core.text_splitter import split_documents
from core.embeddings import create_retriver_from_documents
from core.rag_chain import create_rag_chain
from ui.handlers import StreamHandler, PostMessageHandler

# Configurer les cles API
setup_environment()

# Configurer la page Streamlit
st.set_page_config(
    page_title="PDF QA Chatbot",
    page_icon= "🤖",
    layout= "wide"
)
st.title("Chatbot RAG - Questions sur vos PDFs")

@st.cache_resource(ttl="1h")
def configure_retriever(uploaded_files):
    """
    Pipeline complet : PDF -> Chunks -> Embeddings -> Retriver
    Mis en cache pendant 1 heure
    """
    with st.spinner('Chargement des documents...'):
        documents = load_upploaded_files(uploaded_files)

    with st.spinner('Découpage en chunks...'):
        chunks = split_documents(documents)

    with st.spinner("Création des embeddings..."):
        retriver = create_retriver_from_documents(chunks)

    return retriver

# -----------Interface Utilisateur------------
with st.sidebar:
    st.header("📁 Documents")
    uploaded_files = st.file_uploader("Uploader vos fichiers PDFs", type=["pdf"],
                                      accept_multiple_files=True
                                      )
    if uploaded_files:
        st.success(f"{len(uploaded_files)} fichier(s) chargé(s)")
    st.markdown("---")

    # Section Paramètres du modèle
    st.header("⚙️ Paramètres du Modèle")

    # Sélection du modèle
    selected_model = st.selectbox(
        label= "🤖 Modèle",
        options= AVAILABLE_MODELS,
        index = AVAILABLE_MODELS.index(DEFAULT_MODEL),
        help="Choisissez le modèle GPT à utiliser"
    )

    # Slider de temperature
    selected_temperature = st.slider(
        label="🌡️ Température",
        min_value=0.0,
        max_value=1.0,
        value=DEFAULT_TEMPERATURE,
        step=0.1,
        help="0 = Précis et factuel | 1 = Créatif et variable"
    )
    # Affichage des parametres actuels
    st.markdown("---")
    st.markdown("**📊 Configuration actuelle:**")
    st.code(f"Modèle: {selected_model}\nTempérature: {selected_temperature}")

# Verifier si des fichiers sont uploadés
if not uploaded_files:
    st.info("Veuillez uploader des documents PDF pour commencer.")
    st.stop()

# le retriver (mis en cache)
retriever = configure_retriever(uploaded_files)

# Céer la chaine RAG
rag_chain = create_rag_chain(
    retriever=retriever,
model_name= selected_model,
temperature= selected_temperature
)

# Stocker l'historique dans la session Streamlit
message_history = StreamlitChatMessageHistory(key="chat_messages")
if len(message_history.messages) == 0:
    message_history.add_ai_message(
        "Bonjour ! Je suis prêt à répondre à vos questions sur les documents uploadés."
    )

# Affichage de l'historique des messages
for msg in message_history.messages:
    st.chat_message(msg.type).write(msg.content)
# Chat
if user_question := st.chat_input("Posez votre question..."):
    st.chat_message("human").write(user_question)

    # Génèrer et afficher la réponse
    with st.chat_message("ai"):
        # Container pour le streaming
        stream_container = st.empty()
        # Handlers
        stream_handler = StreamHandler(stream_container)
        source_handler = PostMessageHandler()

        # Configuration callbacks
        config = {"callbacks": [stream_handler, source_handler]}

        # Appel de la chaine RAG
        response = rag_chain.invoke(
            {"question": user_question},
            config=config
        )
    # Sauvegarder dans l'historique

    message_history.add_user_message(user_question)
    message_history.add_ai_message(response.content)