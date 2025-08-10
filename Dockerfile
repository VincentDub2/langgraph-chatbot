# Utiliser une image Python officielle comme base
FROM python:3.12-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration uv
COPY pyproject.toml uv.lock ./

# Installer les dépendances avec uv
RUN uv sync --frozen --no-cache

# Copier le code source
COPY . .

# Créer le répertoire pour les fichiers ICS
RUN mkdir -p ics_out

# Exposer le port
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Commande par défaut
CMD ["uv", "run", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
