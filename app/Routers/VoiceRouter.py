from fastapi import APIRouter, UploadFile, File, Depends, WebSocket
router = APIRouter(
    prefix="/api/voice",
    tags=["Voice"]
)
@router.websocket("/recognize-voice")
async def recognize_voice(websocket:WebSocket):
    return "ok"