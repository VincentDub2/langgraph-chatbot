"""
Routes de gestion des threads de conversation
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException

from src.core.models import ThreadInfo

router = APIRouter(prefix="/threads", tags=["Threads"])


@router.get("/{thread_id}", response_model=ThreadInfo)
async def get_thread_info(thread_id: str):
    """
    Obtenir les informations d'un thread de conversation
    """
    try:
        # Note: Dans une implémentation complète, vous stockeriez les threads en base
        # Pour cette démo, on retourne des informations simulées
        return ThreadInfo(
            thread_id=thread_id,
            created_at=datetime.now().isoformat(),
            message_count=1  # À implémenter avec un vrai stockage
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Thread non trouvé: {str(e)}")


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str):
    """
    Supprimer un thread de conversation
    """
    try:
        # Note: Dans une implémentation complète, vous supprimeriez le thread de la base
        return {"message": f"Thread {thread_id} supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Thread non trouvé: {str(e)}")
