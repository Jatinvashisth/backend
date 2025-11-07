from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

connections: list[WebSocket] = []

@router.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            data = await ws.receive_text()
            # broadcast to all connected clients
            for conn in connections:
                await conn.send_text(f"{data}")
    except WebSocketDisconnect:
        connections.remove(ws)



