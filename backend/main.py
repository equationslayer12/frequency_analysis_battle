# from flask import Flask, jsonify
# from flask_cors import CORS
from fastapi import FastAPI, WebSocket
from protocol import Protocol
from routers import signup, freqrace

app = FastAPI()
app.include_router(signup.router)
app.include_router(freqrace.router)

a = 0

@app.get("/api/test_socket")
def test_socket_http():
    return "This is a real request thank you"


@app.websocket("/api/test_socket_test")
async def test_socket(websocket: WebSocket):
    await websocket.accept()

    text1 = await websocket.receive_text()
    print(text1)
    text2 = await websocket.receive_text()
    print(text2)
    await websocket.send_text("GET SCAMMED")


@app.post("/api/test")
def test():
    global a
    a += 1
    return str(a)


@app.get("/api/test")
def get_test():
    return str(a)
