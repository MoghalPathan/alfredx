from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Alfredx Backend v1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Alfredx Backend Online", "version": "1.0"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("✅ Client connected")
    
    try:
        while True:
            # Receive message from frontend
            message = await websocket.receive_text()
            logger.info(f"📩 Received: {message}")
            
            # Simple echo reply (Phase 1)
            reply = f"Alfredx received: {message}"
            
            # Send back to frontend
            await websocket.send_text(reply)
            logger.info(f"📤 Sent: {reply}")
            
    except WebSocketDisconnect:
        logger.info("❌ Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
