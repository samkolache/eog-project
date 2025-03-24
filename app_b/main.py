from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    sender: str
    text: str

@app.post("/receive")
def receive_message(msg: Message):
    print(f"Received message from {msg.sender}: {msg.text}")
    return {"status": "received", "echo": msg.text}
