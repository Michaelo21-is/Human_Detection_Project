from fastapi import APIRouter, Depends, File, UploadFile, WebSocket, Request, Form
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
@router.post("/save-person")
async def save_person(
    request: Request,
    name: str = Form(...),
    where_is_known_from: str = Form(...),
    face: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    print("has been called")
    session_id = request.cookies.get("session_id")
    data = SetUpRecognizePeopleSchema(
        name=name,
        where_is_known_from=where_is_known_from
    )

    return await llmService.save_person(data, db, session_id, face)

