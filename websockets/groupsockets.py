from fastapi import FastAPI, WebSocket, WebSocketDisconnect

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def direct_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


app = FastAPI()
manager = ConnectionManager()

@app.websocket("/communicate")
async def socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.direct_message(f"message received", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.direct_message("bye", websocket)