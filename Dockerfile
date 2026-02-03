FROM python:3.11-slim

# Repertoire de travail
WORKDIR /app

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copier les requirements
COPY requirements.txt .

# Installer les dependances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Creer le dossier pour ChromaDB
RUN mkdir -p /app/data/chroma_db

# Port Streamlit
EXPOSE 8501

# Command de demarrage
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]