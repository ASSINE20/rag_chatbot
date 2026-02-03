# Clés API, configurations
import os
import yaml

# Charger les cles API depuis le fichier YAML
def load_api_keys(filepath="api_keys.yml"):
    with open(filepath, 'r') as file:
        api_creds = yaml.safe_load(file)
        return api_creds

# Configurer les variables d'environnement
def setup_environment():
    api_creds = load_api_keys()
    os.environ['OPENAI_API_KEY'] = api_creds['OPENAI_API_KEY']

# Parametres du RAG
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
RETRIEVER_K = 5
CHROMA_PATH = "./data/chroma_db"

# Parametres par defaut
DEFAULT_MODEL = "gpt-5-mini"
DEFAULT_TEMPERATURE = 0.5

# Liste des modeles disponibles
AVAILABLE_MODELS = [
    "gpt-5-mini",
    "gpt-5.2",
    "gpt-5-nano"
]