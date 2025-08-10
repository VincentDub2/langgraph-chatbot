"""
Routes de chat pour l'API
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk

from src.core.models import ChatRequest, ChatResponse, ChatStreamRequest
from src.graph.builder import graph

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
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


@router.post("/stream")
async def chat_stream(req: ChatStreamRequest):
    """Endpoint de streaming pour le chat"""
    async def event_gen():
        state = req.graph_state or {"messages":[{"role":"system","content":"You are helpful."}]}
        state["messages"] = state.get("messages", []) + [{"role":"user","content":req.user_input.strip()}]
        cfg = {"configurable":{"thread_id": req.thread_id or str(uuid.uuid4())}}

        async for stream_mode, chunk in graph.astream(
            state, 
            config=cfg, 
            version="v1",
            stream_mode=["messages"]
        ):
            if isinstance(chunk, AIMessageChunk):
                yield f"data: {chunk.model_dump_json()}\n\n"
            else:
                yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_gen(), 
        media_type="text/event-stream",
        headers={"Cache-Control":"no-cache","Connection":"keep-alive"}
    )
