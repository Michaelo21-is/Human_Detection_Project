# משדרים לו תמונות
#
# לשמנור ארדם מסויים
import cv2
import numpy as np
from fastapi import File, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from deepface import DeepFace
import asyncio
from datetime import datetime, timezone, timedelta

from app.Models.UsersModel import User
from app.Models.RecognizedPeopleModel import  RecognizedPeople
from app.Models.UsersRecognizedPeopleMapping import UsersRecognizedPeopleMapper
from app.Schema.SetUpRecognizePeopleSchema import SetUpRecognizePeopleSchema
from app.Models.PersonTimeoutModel import PersonTimeout

class llmService:
    @staticmethod
    def cosine_distance(embedding1, embedding2):
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)

        return 1 - np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

    @staticmethod
    async def find_person(web_socket: WebSocket, db: Session):
        await web_socket.accept()

        session_id = web_socket.cookies.get("session_id")

        if not session_id:
            await web_socket.send_json({
                "success": False,
                "message": "Missing session_id"
            })
            await web_socket.close()
            return

        user = db.query(User).filter(User.session_id == session_id).first()

        if not user:
            await web_socket.send_json({
                "success": False,
                "message": "User not found"
            })
            await web_socket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        try:
            while True:
                message = await web_socket.receive_bytes()

                nparr = np.frombuffer(message, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if img is None:
                    await web_socket.send_json({
                        "success": False,
                        "message": "Invalid image"
                    })
                    continue

                faces = await asyncio.to_thread(
                    DeepFace.represent,
                    img,
                    model_name="VGG-Face",
                    enforce_detection=False
                )

                if not faces:
                    await web_socket.send_json({
                        "success": False,
                        "message": "No face detected"
                    })
                    continue

                embeddings = [face_result["embedding"] for face_result in faces]

                recognizedPeople = (
                    db.query(RecognizedPeople)
                    .join(
                        UsersRecognizedPeopleMapper,
                        UsersRecognizedPeopleMapper.recognized_people_id == RecognizedPeople.id
                    )
                    .filter(UsersRecognizedPeopleMapper.user_id == user.id)
                    .all()
                )

                if not recognizedPeople:
                    await web_socket.send_json({
                        "success": False,
                        "message": "No recognized people saved for this user"
                    })
                    continue

                personInfo = {
                    "name": [],
                    "whereIsKnownFrom": [],
                }
                personId = 0
                for person in recognizedPeople:
                    for embedding in embeddings:
                        distance = llmService.cosine_distance(
                            embedding,
                            person.face_embedding
                        )

                        if distance < 0.4:
                            personInfo["name"].append(person.name)
                            personInfo["whereIsKnownFrom"].append(person.where_is_known_from)
                            personId = person.id
                            break
                if not personInfo["name"]:
                    await web_socket.send_json({
                        "success": False,
                        "message": "No recognized people found"
                    })
                else:
                    if not llmService.can_speak_about_person(db, personId):
                        await web_socket.send_json({
                            "success": False,
                            "message": "this person currently in timeout"
                        })
                        continue
                        # to skip the success message
                    await web_socket.send_json({
                        "success": True,
                        "data": personInfo
                    })

        except WebSocketDisconnect:
            return
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
        friendFace = (
            db.query(RecognizedPeople)
            .join(
                UsersRecognizedPeopleMapper,
                UsersRecognizedPeopleMapper.recognized_people_id == RecognizedPeople.id
            )
            .filter(UsersRecognizedPeopleMapper.user_id == user.id)
            .all()
        )
        for friend in friendFace:
            distance = llmService.cosine_distance(face["embedding"], friend.face_embedding)
            if distance < 0.4:
                return "פרצוף זה מוכר במערכת אין צורך בלהוסיף אותו שוב"
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
        db.commit()
        db.refresh(userRecognizedPeople)
        return "השמירה צלחה"

    @staticmethod
    def can_speak_about_person(db: Session, person_id: int) -> bool:
        timeout_minutes = 10
        now = datetime.now(timezone.utc)

        person_timeout = (
            db.query(PersonTimeout)
            .filter(PersonTimeout.recognized_person_id == person_id)
            .first()
        )

        if person_timeout is None:
            person_timeout = PersonTimeout(
                recognized_person_id=person_id
            )
            db.add(person_timeout)
            db.commit()
            return True

        if now - person_timeout.last_spoken_at >= timedelta(minutes=timeout_minutes):
            # if they are talk before is just gonna update the time they spoke
            person_timeout.last_spoken_at = now
            db.commit()
            return True

        return False
