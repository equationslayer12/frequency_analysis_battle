# from flask import Flask, jsonify
# from flask_cors import CORS
from fastapi import FastAPI, WebSocket
from protocol import Protocol
from routers import signup, freqrace, testing

app = FastAPI()
app.include_router(signup.router)
app.include_router(freqrace.router)
app.include_router(testing.router)