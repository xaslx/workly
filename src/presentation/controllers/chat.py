from fastapi import HTTPException, WebSocket, WebSocketDisconnect, APIRouter, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from datetime import datetime
from src.domain.chat.entity import ChatMessagesEntity
from src.application.use_cases.chat.save_message import SaveMessageUseCase
from src.presentation.schemas.chat.message import Message
from src.application.dto.chat.message import SaveMessageDTO

ws_router = APIRouter()
router = APIRouter()
active_connections = []

async def broadcast_message(data: dict):
    for connection in active_connections:
        try:
            await connection.send_json(data)
        except:
            active_connections.remove(connection)

@ws_router.websocket('/ws/chat')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await broadcast_message(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        active_connections.remove(websocket)


@router.post('/chat/messages')
@inject
async def save_message(
    message: Message,
    use_case: Depends[SaveMessageUseCase],
):
    print(f"Received message: {message}")
    
    message_dto = SaveMessageDTO(
        text=message.text,
        username=message.username,
        created_at=message.created_at,
    )
    
    try:
        saved = await use_case.execute(message_dto)
        print(f"Save result: {saved}")
        
        if not saved:
            raise HTTPException(status_code=500, detail="Failed to save message")
            
        await broadcast_message({
            "text": message.text,
            "username": message.username,
            "created_at": message.created_at.isoformat(),
        })
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
