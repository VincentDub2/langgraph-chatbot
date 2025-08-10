"""
Routes de santé et racine de l'API
"""
from datetime import datetime
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "Chatbot Agent Immobilier API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@router.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
