from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional


class PromptManager:
    """Load Markdown prompt templates by name and version.

    Prompts are stored in a directory with files named ``{name}_v{version}.md``.
    The highest numeric version is considered the latest.
    """

    def __init__(self, directory: str = "prompts") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _version_key(self, path: Path) -> int:
        stem = path.stem
        if "_v" in stem:
            try:
                return int(stem.rsplit("_v", 1)[1])
            except ValueError:
                pass
        return 0

    def available_versions(self, name: str) -> List[int]:
        """Return all available versions for ``name`` sorted ascending."""
        files = self.directory.glob(f"{name}_v*.md")
        versions = [self._version_key(p) for p in files]
        return sorted(v for v in versions if v)

    def load(self, name: str, version: Optional[int] = None) -> str:
        """Load a prompt by ``name`` and ``version``.

        If ``version`` is ``None``, the highest available version is loaded.
        """
        if version is None:
            versions = self.available_versions(name)
            if not versions:
                raise FileNotFoundError(f"No prompt versions found for '{name}'")
            version = versions[-1]
        path = self.directory / f"{name}_v{version}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt '{name}' version {version} not found")
        return path.read_text(encoding="utf-8")


def load_system_prompt(version: str = "v1") -> Optional[str]:
    """
    Charge le prompt système depuis le fichier correspondant.
    
    Args:
        version: Version du prompt (ex: "v1", "v2")
    
    Returns:
        Le contenu du prompt système ou None si le fichier n'existe pas
    """
    prompt_file = f"prompts/chatbot_{version}.md"
    
    if not os.path.exists(prompt_file):
        print(f"Fichier de prompt non trouvé: {prompt_file}")
        return None
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du prompt: {e}")
        return None

def get_default_system_prompt() -> str:
    """
    Retourne un prompt système par défaut si aucun fichier n'est trouvé.
    
    Returns:
        Prompt système par défaut
    """
    return """Vous êtes un assistant virtuel spécialisé dans la gestion des rendez-vous pour une agence immobilière. 

Votre mission principale est d'aider les clients à réserver des créneaux de visite de biens immobiliers avec les agents de l'agence.

Vous devez :
1. Accueillir chaleureusement les clients
2. Collecter leurs informations (nom, email, préférences)
3. Suggérer des agents et des propriétés selon leurs besoins
4. Vérifier les disponibilités des agents
5. Créer des rendez-vous de visite
6. Fournir des confirmations détaillées

Soyez professionnel, courtois et efficace dans vos réponses."""
