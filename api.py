from calendar import c
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import asyncio
import uuid
from datetime import datetime
import os
from langchain_core.messages import AIMessageChunk


from graph import graph
from prompt_manager import load_system_prompt, get_default_system_prompt

# Configuration de l'API
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
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class ChatMessage(BaseModel):
    role: str = Field(..., description="Rôle du message (user, assistant, system)")
    content: str = Field(..., description="Contenu du message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="Message de l'utilisateur")
    thread_id: Optional[str] = Field(None, description="ID du thread de conversation")
    stream: bool = Field(False, description="Activer le streaming de la réponse")

class ChatStreamRequest(BaseModel):
    """
    Requête pour démarrer un streaming de conversation.
    """
    user_input: str = Field(..., description="Texte envoyé par l'utilisateur.")
    thread_id: Optional[str] = Field(
        None,
        description="Identifiant du thread de conversation. Généré si absent."
    )
    graph_state: Optional[Dict[str, Any]] = Field(
        None,
        description="État courant du graphe (messages + autres infos LangGraph)."
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="Réponse du chatbot")
    thread_id: str = Field(..., description="ID du thread de conversation")
    timestamp: str = Field(..., description="Timestamp de la réponse")

class ThreadInfo(BaseModel):
    thread_id: str = Field(..., description="ID du thread")
    created_at: str = Field(..., description="Date de création")
    message_count: int = Field(..., description="Nombre de messages")

class AgentInfo(BaseModel):
    id: str = Field(..., description="ID de l'agent")
    name: str = Field(..., description="Nom de l'agent")
    specialities: List[str] = Field(..., description="Spécialités de l'agent")
    languages: List[str] = Field(..., description="Langues parlées")

class PropertyInfo(BaseModel):
    id: str = Field(..., description="ID de la propriété")
    title: str = Field(..., description="Titre de la propriété")
    type: str = Field(..., description="Type de propriété")
    price: float = Field(..., description="Prix")
    location: str = Field(..., description="Localisation")
    surface: float = Field(..., description="Surface en m²")
    rooms: int = Field(..., description="Nombre de pièces")
    bedrooms: int = Field(..., description="Nombre de chambres")

class AvailabilityRequest(BaseModel):
    agent_id: str = Field(..., description="ID de l'agent")
    window: str = Field(..., description="Période de recherche (ex: 'today', 'tomorrow afternoon')")

class AppointmentRequest(BaseModel):
    agent_id: str = Field(..., description="ID de l'agent")
    start: str = Field(..., description="Date/heure de début (ISO format)")
    end: str = Field(..., description="Date/heure de fin (ISO format)")
    title: str = Field(..., description="Titre du rendez-vous")
    attendees: Optional[List[Dict[str, str]]] = Field(None, description="Liste des participants")
    location: Optional[str] = Field(None, description="Adresse du bien")
    description: Optional[str] = Field(None, description="Description du rendez-vous")

# Routes de l'API

@app.get("/", tags=["Root"])
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "Chatbot Agent Immobilier API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Envoyer un message au chatbot et recevoir une réponse
    """
    try:
        # Créer ou récupérer le thread
        thread_id = request.thread_id or str(uuid.uuid4())
        
        # Préparer les messages pour le graph
        messages = [{"role": "user", "content": request.message}]
        
        # Exécuter le graph
        config = {"configurable": {"thread_id": thread_id}}
        result = graph.invoke({"messages": messages}, config)
        
        # Extraire la réponse
        response_content = ""
        for message in result["messages"]:
            if hasattr(message, 'content') and message.content:
                response_content += str(message.content)
        
        return ChatResponse(
            response=response_content,
            thread_id=thread_id,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(req: ChatStreamRequest):
    async def event_gen():
        state = req.graph_state or {"messages":[{"role":"system","content":"You are helpful."}]}
        state["messages"] = state.get("messages", []) + [{"role":"user","content":req.user_input.strip()}]
        cfg = {"configurable":{"thread_id": req.thread_id or str(uuid.uuid4())}}

        async for stream_mode, chunk  in graph.astream(
            state, 
            config=cfg, 
            version="v1",
            stream_mode=["messages"]
        ):
            if isinstance(chunk, AIMessageChunk):
                yield f"data: {chunk.model_dump_json()}\n\n"
            else:
                yield f"data: {chunk}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream",
                             headers={"Cache-Control":"no-cache","Connection":"keep-alive"})




@app.get("/threads/{thread_id}", response_model=ThreadInfo, tags=["Threads"])
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

@app.delete("/threads/{thread_id}", tags=["Threads"])
async def delete_thread(thread_id: str):
    """
    Supprimer un thread de conversation
    """
    try:
        # Note: Dans une implémentation complète, vous supprimeriez le thread de la base
        return {"message": f"Thread {thread_id} supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Thread non trouvé: {str(e)}")

@app.get("/agents", response_model=List[AgentInfo], tags=["Agents"])
async def list_agents():
    """
    Lister tous les agents disponibles
    """
    try:
        from tools import list_agents as list_agents_tool
        agents_data = list_agents_tool()
        
        agents = []
        for agent in agents_data:
            agents.append(AgentInfo(
                id=agent["id"],
                name=agent["name"],
                specialities=agent["specialities"],
                languages=agent["languages"]
            ))
        
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des agents: {str(e)}")

@app.get("/agents/{agent_id}", response_model=AgentInfo, tags=["Agents"])
async def get_agent_info(agent_id: str):
    """
    Obtenir les informations détaillées d'un agent
    """
    try:
        from tools import get_agent_info as get_agent_info_tool
        agent_data = get_agent_info_tool(agent_id)
        
        if "error" in agent_data:
            raise HTTPException(status_code=404, detail=agent_data["error"])
        
        return AgentInfo(
            id=agent_data["id"],
            name=agent_data["name"],
            specialities=agent_data["specialities"],
            languages=agent_data["languages"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'agent: {str(e)}")

@app.get("/properties", response_model=List[PropertyInfo], tags=["Properties"])
async def list_properties(
    property_type: Optional[str] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None
):
    """
    Lister les propriétés avec filtres optionnels
    """
    try:
        from tools import list_properties as list_properties_tool
        properties_data = list_properties_tool(property_type, max_price, location)
        
        properties = []
        for prop in properties_data:
            properties.append(PropertyInfo(
                id=prop["id"],
                title=prop["title"],
                type=prop["type"],
                price=prop["price"],
                location=prop["location"],
                surface=prop["surface"],
                rooms=prop["rooms"],
                bedrooms=prop["bedrooms"]
            ))
        
        return properties
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des propriétés: {str(e)}")

@app.get("/properties/{property_id}", response_model=PropertyInfo, tags=["Properties"])
async def get_property_info(property_id: str):
    """
    Obtenir les informations détaillées d'une propriété
    """
    try:
        from tools import get_property_info as get_property_info_tool
        property_data = get_property_info_tool(property_id)
        
        if "error" in property_data:
            raise HTTPException(status_code=404, detail=property_data["error"])
        
        return PropertyInfo(
            id=property_data["id"],
            title=property_data["title"],
            type=property_data["type"],
            price=property_data["price"],
            location=property_data["location"],
            surface=property_data["surface"],
            rooms=property_data["rooms"],
            bedrooms=property_data["bedrooms"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la propriété: {str(e)}")

@app.post("/availability", tags=["Appointments"])
async def check_availability(request: AvailabilityRequest):
    """
    Vérifier les disponibilités d'un agent
    """
    try:
        from tools import check_availability as check_availability_tool
        availability_data = check_availability_tool(request.agent_id, request.window)
        
        return {
            "agent_id": request.agent_id,
            "window": request.window,
            "slots": availability_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification des disponibilités: {str(e)}")

@app.post("/appointments", tags=["Appointments"])
async def create_appointment(request: AppointmentRequest):
    """
    Créer un nouveau rendez-vous
    """
    try:
        from tools import create_event as create_event_tool
        from datetime import datetime
        
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

@app.get("/search/properties", tags=["Search"])
async def search_properties(
    type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_surface: Optional[float] = None,
    max_surface: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    location: Optional[str] = None,
    agent_id: Optional[str] = None
):
    """
    Recherche avancée de propriétés
    """
    try:
        from tools import search_properties_by_criteria as search_properties_tool
        
        criteria = {}
        if type:
            criteria["type"] = type
        if min_price:
            criteria["min_price"] = min_price
        if max_price:
            criteria["max_price"] = max_price
        if min_surface:
            criteria["min_surface"] = min_surface
        if max_surface:
            criteria["max_surface"] = max_surface
        if min_bedrooms:
            criteria["min_bedrooms"] = min_bedrooms
        if location:
            criteria["location"] = location
        if agent_id:
            criteria["agent_id"] = agent_id
        
        properties_data = search_properties_tool(criteria)
        
        properties = []
        for prop in properties_data:
            properties.append(PropertyInfo(
                id=prop["id"],
                title=prop["title"],
                type=prop["type"],
                price=prop["price"],
                location=prop["location"],
                surface=prop["surface"],
                rooms=prop["rooms"],
                bedrooms=prop["bedrooms"]
            ))
        
        return {
            "criteria": criteria,
            "count": len(properties),
            "properties": properties
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
