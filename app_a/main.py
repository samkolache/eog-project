from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/send")
def send_message():
    message = {"sender": "App A", "text": "Hello from App A!"}
    response = httpx.post("http://app_b:8000/receive", json=message)
    return {"app_b_response": response.json()}
