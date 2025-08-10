"""
Routes de gestion des rendez-vous
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException

from src.core.models import AvailabilityRequest, AppointmentRequest
from tools import (
    check_availability as check_availability_tool,
    create_event as create_event_tool
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/availability")
async def check_availability(request: AvailabilityRequest):
    """
    Vérifier les disponibilités d'un agent
    """
    try:
        availability_data = check_availability_tool(request.agent_id, request.window)
        
        return {
            "agent_id": request.agent_id,
            "window": request.window,
            "slots": availability_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification des disponibilités: {str(e)}")


@router.post("/")
async def create_appointment(request: AppointmentRequest):
    """
    Créer un nouveau rendez-vous
    """
    try:
        # Convertir les dates
        start_dt = datetime.fromisoformat(request.start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(request.end.replace('Z', '+00:00'))
        
        event_data = create_event_tool(
            agent_id=request.agent_id,
            start=start_dt,
            end=end_dt,
            title=request.title,
            attendees=request.attendees,
            location=request.location,
            description=request.description
        )
        
        return {
            "message": "Rendez-vous créé avec succès",
            "event": event_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du rendez-vous: {str(e)}")
