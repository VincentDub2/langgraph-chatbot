# Refactorisation du Projet Chatbot Immobilier

## Vue d'ensemble

Ce projet a été entièrement refactorisé pour améliorer l'organisation, la maintenabilité et la scalabilité du code.

## Nouvelle Structure

```
langgraph-chatbot/
├── src/                          # Code source principal
│   ├── core/                     # Composants centraux
│   │   ├── config.py            # Configuration centralisée
│   │   ├── models.py            # Modèles Pydantic
│   │   └── prompts.py           # Gestion des prompts
│   ├── graph/                   # Logique LangGraph
│   │   ├── tools.py             # Outils LangGraph
│   │   └── builder.py           # Construction du graphe
│   ├── api/                     # API FastAPI
│   │   ├── app.py               # Application principale
│   │   └── routes/              # Routes organisées par domaine
│   │       ├── chat.py          # Routes de chat
│   │       ├── threads.py       # Gestion des threads
│   │       ├── agents.py        # Gestion des agents
│   │       ├── properties.py    # Gestion des propriétés
│   │       ├── appointments.py  # Gestion des rendez-vous
│   │       └── health.py        # Routes de santé
│   ├── cli/                     # Interface en ligne de commande
│   │   └── app.py               # Application CLI
│   └── ui/                      # Interfaces utilisateur
│       └── gradio_app.py        # Interface Gradio
├── tools/                       # Outils métier (inchangé)
├── prompts/                     # Fichiers de prompts (inchangé)
├── main.py                      # Point d'entrée API
├── cli.py                       # Point d'entrée CLI
├── gradio_app.py                # Point d'entrée Gradio
└── api.py                       # Ancien fichier API (à supprimer)
```

## Améliorations apportées

### 1. Séparation des responsabilités
- **Configuration centralisée** : Tous les paramètres dans `src/core/config.py`
- **Modèles isolés** : Tous les modèles Pydantic dans `src/core/models.py`
- **Routes modulaires** : Chaque domaine a ses propres routes

### 2. Architecture modulaire
- **Package `core`** : Composants centraux réutilisables
- **Package `graph`** : Logique LangGraph séparée
- **Package `api`** : API organisée par domaines
- **Package `cli`** : Interface en ligne de commande
- **Package `ui`** : Interfaces utilisateur

### 3. Points d'entrée clairs
- `main.py` : Lance l'API FastAPI
- `cli.py` : Lance l'interface CLI
- `gradio_app.py` : Lance l'interface Gradio

### 4. Configuration améliorée
- Gestion centralisée des variables d'environnement
- Configuration par défaut avec surcharge possible
- Validation des paramètres avec Pydantic

## Migration

### Ancien → Nouveau

| Ancien fichier | Nouveau fichier |
|----------------|-----------------|
| `api.py` | `src/api/app.py` + `src/api/routes/*.py` |
| `graph.py` | `src/graph/builder.py` + `src/graph/tools.py` |
| `prompt_manager.py` | `src/core/prompts.py` |
| `app.py` | `src/cli/app.py` |

### Commandes de lancement

```bash
# API FastAPI
python main.py

# Interface CLI
python cli.py

# Interface Gradio
python gradio_app.py
```

## Avantages de la refactorisation

1. **Maintenabilité** : Code organisé par domaines fonctionnels
2. **Testabilité** : Modules isolés et testables individuellement
3. **Scalabilité** : Structure modulaire facilitant l'ajout de fonctionnalités
4. **Lisibilité** : Fichiers plus petits et mieux organisés
5. **Réutilisabilité** : Composants centraux réutilisables
6. **Configuration** : Gestion centralisée des paramètres

## Prochaines étapes

1. Supprimer les anciens fichiers (`api.py`, `graph.py`, `prompt_manager.py`, `app.py`)
2. Ajouter des tests unitaires pour chaque module
3. Implémenter la gestion d'erreurs centralisée
4. Ajouter la documentation API automatique
5. Mettre en place un système de logging structuré
