"""
Configuration centralisée du projet
"""
import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv


class Settings(BaseModel):
    """Configuration de l'application"""


    
    # API Keys
    openai_api_key: Optional[str] = None
    mistral_api_key: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    
    # Modèle
    model_name: str = "gpt-oss-120b"
    temperature: float = 0.2
    
    # Serveur
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS
    cors_origins: list = ["*"]
    
    # Chemins
    prompts_dir: str = "prompts"
    logs_dir: str = "logs"
    ics_dir: str = "ics_out"


def get_settings() -> Settings:
    """Retourne l'instance des paramètres"""
    load_dotenv()
    
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
        model_name=os.getenv("MODEL_NAME", "gpt-oss-120b"),
        temperature=float(os.getenv("TEMPERATURE", "0.2")),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
        prompts_dir=os.getenv("PROMPTS_DIR", "prompts"),
        logs_dir=os.getenv("LOGS_DIR", "logs"),
        ics_dir=os.getenv("ICS_DIR", "ics_out")
    )
