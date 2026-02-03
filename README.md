# 🤖 RAG Chatbot - Questions sur vos PDFs

Un chatbot intelligent qui répond à vos questions en analysant vos documents PDF, utilisant la technique RAG (Retrieval Augmented Generation).
---
## 📋 Fonctionnalités

- ✅ Upload de fichiers PDF (simple ou multiple)
- ✅ Analyse intelligente des documents avec RAG
- ✅ Streaming des réponses en temps réel
- ✅ Affichage des sources utilisées
- ✅ Sélection du modèle GPT (gpt-5-mini, gpt-5.2, etc.)
- ✅ Ajustement de la température (créativité)
- ✅ Historique des conversations
- ✅ Déploiement Docker
- ✅ CI/CD avec GitHub Actions
---
## 🏗️ Architecture

```
Question utilisateur
        │
        ▼
┌───────────────┐
│   Retriever   │ ── Recherche les chunks pertinents dans ChromaDB
└───────────────┘
        │
        ▼
┌───────────────┐
│    Prompt     │ ── Combine contexte + question
└───────────────┘
        │
        ▼
┌───────────────┐
│     LLM       │ ── Génère la réponse (GPT-5)
└───────────────┘
        │
        ▼
    Réponse
```
---

## 📁 Structure du Projet

```
rag_chatbot/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration et paramètres
├── core/
│   ├── __init__.py
│   ├── document_loader.py   # Chargement des PDFs
│   ├── text_splitter.py     # Découpage en chunks
│   ├── embeddings.py        # Embeddings + ChromaDB
│   └── rag_chain.py         # Chaîne RAG
├── ui/
│   ├── __init__.py
│   └── handlers.py          # Handlers Streamlit
├── data/
│   └── chroma_db/           # Base de données vectorielle
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # Pipeline CI/CD
├── app.py                   # Application principale
├── Dockerfile               # Image Docker
├── docker-compose.yml       # Orchestration Docker
├── .dockerignore            # Fichiers exclus du build
├── .gitignore               # Fichiers exclus de Git
├── api_keys.yml             # Clés API (non versionné)
├── requirements.txt         # Dépendances Python
└── README.md
```

---

## 📦 Technologies Utilisées

| Technologie | Usage |
|-------------|-------|
| **LangChain** | Framework pour applications LLM |
| **OpenAI GPT-5** | Modèle de langage |
| **ChromaDB** | Base de données vectorielle |
| **Streamlit** | Interface utilisateur |
| **PyMuPDF** | Lecture des fichiers PDF |
| **Docker** | Conteneurisation |
| **GitHub Actions** | CI/CD |
| **GHCR** | Registry d'images Docker |
---
## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/ASSINE20/rag_chatbot.git
cd rag_chatbot
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les clés API

Créer un fichier `api_keys.yml` à la racine :

```yaml
OPENAI_API_KEY: "sk-votre-cle-api-openai"
```

### 5. Lancer l'application

```bash
streamlit run app.py
```
### Utiliser l'image GHCR
```bash
docker pull ghcr.io/ASSINE20/rag_chatbot:latest

docker run -p 8501:8501 -e OPENAI_API_KEY="sk-votre-cle" ghcr.io/ASSINE20/rag_chatbot:latest
```

L'application sera disponible sur `http://localhost:8501`

## 🔄 CI/CD Pipeline

Le projet utilise GitHub Actions pour l'intégration et le déploiement continus.

### Pipeline automatique
---
```
git push main
      │
      ▼
┌─────────────┐
│   BUILD     │ → Checkout, Setup Python, Install deps
└─────────────┘
      │
      ▼
┌─────────────┐
│   TEST      │ → Exécution des tests
└─────────────┘
      │
      ▼
┌─────────────┐
│   DOCKER    │ → Build image, Push to GHCR
└─────────────┘
      │
      ▼
📦 Image disponible sur ghcr.io
```
---
## 🎮 Utilisation

1. **Uploadez** vos fichiers PDF via la barre latérale
2. **Sélectionnez** le modèle GPT souhaité
3. **Ajustez** la température selon vos besoins
4. **Posez** vos questions dans le chat
5. **Consultez** les sources utilisées pour chaque réponse


---

## 👤 By Géraud ASSINE

---