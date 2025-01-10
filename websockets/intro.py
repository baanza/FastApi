from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException
from prophet import llmresponse
from groq import Groq
from dotenv import load_dotenv
import os

with open("response.html", "r") as file:
    response = file.read()

load_dotenv()
app = FastAPI()

client = Groq(
    api_key= os.environ.get("GROQ_API_KEY")
)

@app.get("/")
async def get():
    return HTMLResponse(response)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            print("websocket received the text")
            to_be_sent = llmresponse(data)
            print(f"to be sent created =>{to_be_sent}")
            for info in llmresponse(data):
                await websocket.send_text(f"{str(info)}")
        except WebSocketDisconnect:
            print("disconnected websocket")