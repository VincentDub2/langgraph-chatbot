"""
Modèles Pydantic pour l'API
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatMessage(BaseModel):
    """Modèle pour un message de chat"""
    role: str = Field(..., description="Rôle du message (user, assistant, system)")
    content: str = Field(..., description="Contenu du message")


class ChatRequest(BaseModel):
    """Requête de chat standard"""
    message: str = Field(..., description="Message de l'utilisateur")
    thread_id: Optional[str] = Field(None, description="ID du thread de conversation")
    stream: bool = Field(False, description="Activer le streaming de la réponse")


class ChatStreamRequest(BaseModel):
    """Requête pour le streaming de chat"""
    user_input: str = Field(..., description="Texte envoyé par l'utilisateur")
    thread_id: Optional[str] = Field(
        None, description="Identifiant du thread de conversation"
    )
    graph_state: Optional[Dict[str, Any]] = Field(
        None, description="État courant du graphe"
    )


class ChatResponse(BaseModel):
    """Réponse du chat"""
    response: str = Field(..., description="Réponse du chatbot")
    thread_id: str = Field(..., description="ID du thread de conversation")
    timestamp: str = Field(..., description="Timestamp de la réponse")


class ThreadInfo(BaseModel):
    """Informations sur un thread"""
    thread_id: str = Field(..., description="ID du thread")
    created_at: str = Field(..., description="Date de création")
    message_count: int = Field(..., description="Nombre de messages")


class AgentInfo(BaseModel):
    """Informations sur un agent"""
    id: str = Field(..., description="ID de l'agent")
    name: str = Field(..., description="Nom de l'agent")
    specialities: List[str] = Field(..., description="Spécialités de l'agent")
    languages: List[str] = Field(..., description="Langues parlées")


class PropertyInfo(BaseModel):
    """Informations sur une propriété"""
    id: str = Field(..., description="ID de la propriété")
    title: str = Field(..., description="Titre de la propriété")
    type: str = Field(..., description="Type de propriété")
    price: float = Field(..., description="Prix")
    location: str = Field(..., description="Localisation")
    surface: float = Field(..., description="Surface en m²")
    rooms: int = Field(..., description="Nombre de pièces")
    bedrooms: int = Field(..., description="Nombre de chambres")


class AvailabilityRequest(BaseModel):
    """Requête de vérification de disponibilité"""
    agent_id: str = Field(..., description="ID de l'agent")
    window: str = Field(..., description="Période de recherche")


class AppointmentRequest(BaseModel):
    """Requête de création de rendez-vous"""
    agent_id: str = Field(..., description="ID de l'agent")
    start: str = Field(..., description="Date/heure de début (ISO format)")
    end: str = Field(..., description="Date/heure de fin (ISO format)")
    title: str = Field(..., description="Titre du rendez-vous")
    attendees: Optional[List[Dict[str, str]]] = Field(None, description="Liste des participants")
    location: Optional[str] = Field(None, description="Adresse du bien")
    description: Optional[str] = Field(None, description="Description du rendez-vous")


class SearchCriteria(BaseModel):
    """Critères de recherche de propriétés"""
    type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_surface: Optional[float] = None
    max_surface: Optional[float] = None
    min_bedrooms: Optional[int] = None
    location: Optional[str] = None
    agent_id: Optional[str] = None


class SearchResponse(BaseModel):
    """Réponse de recherche"""
    criteria: Dict[str, Any]
    count: int
    properties: List[PropertyInfo]
