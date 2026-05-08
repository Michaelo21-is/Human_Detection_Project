# משדרים לו תמונות
#
# לשמנור ארדם מסויים
import cv2
import numpy as np
from fastapi import File, HTTPException, status
from sqlalchemy.orm import Session
from deepface import DeepFace
from app.Models.UsersModel import User
from app.Models.RecognizedPeopleModel import  RecognizedPeople
from app.Models.UsersRecognizedPeopleMapping import UsersRecognizedPeopleMapper
from app.Schema.SetUpRecognizePeopleSchema import SetUpRecognizePeopleSchema

class llmService:
    @staticmethod
    def cosine_distance(embedding1, embedding2):
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)

        return 1 - np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
    @staticmethod
    async def find_person(face: File, db: Session, session_id: str):
        user = db.query(User).filter(User.session_id == session_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        contents = await face.read()

        nparr = np.frombuffer(contents, np.uint8)

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return

        faces = DeepFace.represent(img, model_name="VGG-Face")

        if not faces:
            return

        embeddings = [face_result["embedding"] for face_result in faces]



        userId = user.id

        recognizedPeople = (
            db.query(RecognizedPeople)
            .join(
                UsersRecognizedPeopleMapper,
                UsersRecognizedPeopleMapper.recognized_people_id == RecognizedPeople.id
            )
            .filter(UsersRecognizedPeopleMapper.user_id == userId)
            .all()
        )

        if not recognizedPeople:
            return

        personInfo = {
            "name": [],
            "whereIsKnownFrom": [],
        }

        for person in recognizedPeople:
            for embedding in embeddings:
                distance = llmService.cosine_distance(embedding, person.face_embedding)

                if distance < 0.4:
                    personInfo["name"].append(person.name)
                    personInfo["whereIsKnownFrom"].append(person.where_is_known_from)
                    break

        return personInfo
    @staticmethod
    async def save_person(data: SetUpRecognizePeopleSchema, db: Session, session_id: str, face: File):
        user = db.query(User).filter(User.session_id == session_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        contents = await face.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return "קרה בעייה טכנית בבקשה נסה שוב עוד הפעם"
        face = DeepFace.represent(img, model_name="VGG-Face")
        if not face:
            return "לא זוהה פרצוף"
        if len(face) > 1:
            return "צריך שתעלה תמונה של פרצוף אחד לא יותר כדי שהזיהוי יהיה טוב יותר"
        face = face[0]
        recognizedPeople = RecognizedPeople(
            name=data.name,
            where_is_known_from=data.where_is_known_from,
            face_embedding=face["embedding"]
        )
        db.add(recognizedPeople)
        db.commit()
        db.refresh(recognizedPeople)

        userRecognizedPeople = UsersRecognizedPeopleMapper(user_id=user.id, recognized_people_id=recognizedPeople.id)
        db.add(userRecognizedPeople)

        db.refresh(userRecognizedPeople)
        db.close()
        return "השמירה צלחה"


