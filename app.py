from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from audio import AudioProcessor


app = FastAPI()

class Room(BaseModel):
    name: str


audio_processor = AudioProcessor()

@app.post("/create_room")
async def create_room(room: Room):
    return await audio_processor.create_room(room.name)

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await audio_processor.join_room(websocket, room_name)

@app.get("/")
async def read_root():
    return {"message": "다중 채팅방 지원 실시간 오디오 처리 서버"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=24015)

