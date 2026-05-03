from fastapi import APIRouter, Depends, File, UploadFile, Header
from sqlalchemy.orm import Session
from app.database import get_db


router = APIRouter(
    prefix="/api/llm",
    tags=["Llm"]
)
@router.post("/check-face")
def check_face(db: Session = Depends(get_db) ,face: UploadFile= File(...), session_id: str = Header(...)):


