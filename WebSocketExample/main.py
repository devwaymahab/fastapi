from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
import json

connections = []

app = FastAPI()


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()

    user_connection = {"user": username, "websocket": websocket}
    connections.append(user_connection)
    try:
        while True:

            data = await websocket.receive_text()

            for connection in connections:

                await connection["websocket"].send_text(
                    json.dumps({"sender": username, "message": data})
                )
    except WebSocketDisconnect:

        connections.remove(user_connection)

        print(f"{username} disconnected")
