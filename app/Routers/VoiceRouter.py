from fastapi import APIRouter, UploadFile, File, Depends, WebSocket
from sqlalchemy.orm import Session
from app.database import get_db
from app.Services.VoiceService import VoiceService
router = APIRouter(
    prefix="/api/voice",
    tags=["Voice"]
)
@router.websocket("/recognize-voice")
async def recognize_voice(websocket:WebSocket):
    return VoiceService.recognize_voice(websocket)