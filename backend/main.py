# FastAPI + WebSocket (code from before)

from fastapi import FastAPI, WebSocket
from langdetect import detect
from googletrans import Translator
import asyncio

app = FastAPI()
translator = Translator()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        lang = detect(data)
        # Process command (your brain logic here later)
        reply = f"Understood in {lang}: {data}"  # Turkish/English reply
        if lang != 'en':
            reply = translator.translate(reply, dest='en' if lang == 'tr' else 'tr').text
        await websocket.send_text(reply)
