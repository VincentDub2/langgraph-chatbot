"""
Application FastAPI principale
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.api.routes import chat, threads, agents, properties, appointments, health

def create_app() -> FastAPI:
    """Crée et configure l'application FastAPI"""
    settings = get_settings()
    
    app = FastAPI(
        title="Chatbot Agent Immobilier API",
        description="API pour la gestion des rendez-vous immobiliers avec chatbot intelligent",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configuration CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inclusion des routes
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(threads.router)
    app.include_router(agents.router)
    app.include_router(properties.router)
    app.include_router(appointments.router)

    return app


# Instance de l'application
app = create_app()
