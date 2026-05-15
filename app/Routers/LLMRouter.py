from fastapi import APIRouter, Depends, File, UploadFile, Header, WebSocket, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.Services.llmService import llmService
from app.Schema.SetUpRecognizePeopleSchema import SetUpRecognizePeopleSchema


router = APIRouter(
    prefix="/api/llm",
    tags=["Llm"]
)
@router.websocket("/check-face")
async def check_face(web_socket: WebSocket, db: Session = Depends(get_db)):
    await llmService.find_person(web_socket, db)
def save_person(data: SetUpRecognizePeopleSchema, db: Session = Depends(get_db), face: UploadFile = File(...), request: Request = Request):
    session_id = request.cookies.get("session_id")
    return llmService.save_person(data, db, session_id, face)

