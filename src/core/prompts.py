"""
Gestion des prompts système
"""
import os
from pathlib import Path
from typing import List, Optional
from src.core.config import get_settings


class PromptManager:
    """Gestionnaire de prompts avec versioning"""

    def __init__(self, directory: Optional[str] = None) -> None:
        settings = get_settings()
        self.directory = Path(directory or settings.prompts_dir)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _version_key(self, path: Path) -> int:
        """Extrait la version d'un fichier de prompt"""
        stem = path.stem
        if "_v" in stem:
            try:
                return int(stem.rsplit("_v", 1)[1])
            except ValueError:
                pass
        return 0

    def available_versions(self, name: str) -> List[int]:
        """Retourne toutes les versions disponibles pour un nom"""
        files = self.directory.glob(f"{name}_v*.md")
        versions = [self._version_key(p) for p in files]
        return sorted(v for v in versions if v)

    def load(self, name: str, version: Optional[int] = None) -> str:
        """Charge un prompt par nom et version"""
        if version is None:
            versions = self.available_versions(name)
            if not versions:
                raise FileNotFoundError(f"Aucune version trouvée pour '{name}'")
            version = versions[-1]
        
        path = self.directory / f"{name}_v{version}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt '{name}' version {version} non trouvé")
        
        return path.read_text(encoding="utf-8")


def load_system_prompt(version: str = "v1") -> Optional[str]:
    """Charge le prompt système depuis le fichier correspondant"""
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
    """Retourne un prompt système par défaut"""
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


# Instance globale du gestionnaire de prompts
prompt_manager = PromptManager()
