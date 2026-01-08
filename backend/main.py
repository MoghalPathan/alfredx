from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import sys
import os

# Add core to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.winter_soldier import WinterSoldierProtocol
from core.voice_handler import VoiceHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Alfredx Backend v2.0 - Winter Soldier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
ws_protocol = WinterSoldierProtocol()
voice_handler = VoiceHandler()

@app.get("/")
async def root():
    return {"status": "Alfredx Phase 2: Winter Soldier Online", "version": "2.0"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("✅ Client connected")
    
    # Send initial status
    await websocket.send_json({
        "type": "status",
        "message": "Winter Soldier Protocol active",
        "winter_soldier": ws_protocol.get_status()
    })
    
    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")
            text = data.get("text", "")
            
            logger.info(f"📩 Command: {command}, Text: {text}")
            
            if command == "winter_soldier_check":
                # Check trigger word
                result = ws_protocol.check_word(text)
                await websocket.send_json({
                    "type": "winter_soldier_result",
                    "result": result
                })
                
            elif command == "chat":
                # Normal chat (Phase 1)
                reply = f"Alfredx: {text}"
                await websocket.send_json({
                    "type": "chat_reply",
                    "message": reply
                })
                
            elif command == "voice_listen":
                # Start listening
                voice_result = voice_handler.listen(timeout=5)
                await websocket.send_json({
                    "type": "voice_result",
                    "result": voice_result
                })
                
            elif command == "speak":
                # TTS
                voice_handler.speak(text, data.get("language", "en"))
                await websocket.send_json({
                    "type": "speak_done"
                })
                
    except WebSocketDisconnect:
        logger.info("❌ Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
