from fastapi import APIRouter, Depends, File, UploadFile, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.Services.llmService import llmService
from app.Schema.SetUpRecognizePeopleSchema import SetUpRecognizePeopleSchema


router = APIRouter(
    prefix="/api/llm",
    tags=["Llm"]
)
@router.post("/check-face")
def check_face(db: Session = Depends(get_db) ,face: UploadFile= File(...), session_id: str = Header(...)):
    return llmService.find_person(face, db, session_id)
def save_person(data: SetUpRecognizePeopleSchema, db: Session = Depends(get_db), session_id: str = Header(...), face: UploadFile = File(...)):
    return llmService.save_person(data, db, session_id, face)

