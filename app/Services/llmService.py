# משדרים לו תמונות
#
# לשמנור ארדם מסויים
from fastapi import File
from sqlalchemy.orm import Session
from deepface import DeepFace
from app.Models.UsersModel import User
from app.Models.RecognizedPeopleModel import  RecognizedPeople
from app.Models.UsersRecognizedPeopleMapping import UsersRecognizedPeopleMapper


class llmService:
    def check_is_person(face: File):
        try:
            # trying find face in the picture
            DeepFace.extract_faces(face)
            return True
        except:
            return False

    def find_person(face: File, db:Session, session_id: str):
        isPerson = llmService.check_is_person(face)
        if not isPerson:
            return
        userId = db.query(User).filter(User.session_id == session_id).get(User.id)



