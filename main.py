"""
Point d'entrée principal de l'application
"""
import uvicorn
from src.api.app import app
from src.core.config import get_settings


def main():
    """Lance l'application FastAPI"""
    settings = get_settings()
    
    uvicorn.run(
        "src.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()
