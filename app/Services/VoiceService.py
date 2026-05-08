from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
import speech_recognition as sr
import tempfile



class VoiceService:
    @staticmethod
    async def recognize_voice(websocket: WebSocket):
        await websocket.accept()

        audio_buffer = bytearray()

        try:
            while True:
                message = await websocket.receive()

                if message.get("bytes") is not None:
                    audio_buffer.extend(message["bytes"])

                elif message.get("text") == "END":
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                        temp_audio.write(audio_buffer)
                        temp_audio_path = temp_audio.name

                    recognizer = sr.Recognizer()

                    with sr.AudioFile(temp_audio_path) as source:
                        audio_data = recognizer.record(source)

                    text = recognizer.recognize_google(audio_data, language="he-IL")

                    await websocket.send_text(text)

                    audio_buffer.clear()

        except WebSocketDisconnect:
            return


