# Retrieval Augmented Generation
from langchain_community.chat_models.litellm_router import model_extra_key_name
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter
from config.settings import DEFAULT_MODEL, DEFAULT_TEMPERATURE

def create_llm(model_name: str = DEFAULT_MODEL,
               temperature: float = DEFAULT_TEMPERATURE,
        streaming: bool = True):

    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        streaming=streaming
    )
    return llm

def create_prompt_template():
    template = """
    Utilise uniquement le contexte suivant pour répondre à la question.
    Si tu ne connais pas la réponse, dis simplement que tu ne sais pas.
    Ne fabrique pas de réponse. Sois concis.
    
    Contexte:
    {context}
    
    Question: {question}
    
    Réponse précise:
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt

# Formate les documents récupérés en une seule chaîne de texte
def format_docs(docs: list) -> str:
    return "\n\n".join([doc.page_content for doc in docs])

# Créer la chaîne RAG complète
def create_rag_chain(retriever, model_name: str = DEFAULT_MODEL,
                     temperature: float = DEFAULT_TEMPERATURE):
    llm = create_llm(model_name=model_name, temperature=temperature)
    prompt = create_prompt_template()

    #Construction de la chaine
    rag_chain = (
        {
            # Recuperer les docs pertinents et les formats
            "context": itemgetter("question") | retriever | format_docs,
            # Passe la question
            "question": itemgetter("question")
        }
        |
        prompt # Injecte context + question dans le template
        |
        llm # Envoie au LLM generer la reponse
    )
    return rag_chain