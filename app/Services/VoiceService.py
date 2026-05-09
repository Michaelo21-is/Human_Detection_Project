from fastapi import WebSocket, WebSocketDisconnect
import speech_recognition as sr
import webrtcvad


class VoiceService:
    @staticmethod
    async def recognize_voice(websocket: WebSocket):
        await websocket.accept()
        vad = webrtcvad.Vad(2)
        audio_buffer = bytearray()
        sampleRate = 16000
        text = ""
        excpected_chunk_size = 640
        recognizer = sr.Recognizer()
        silence_chunk = 0
        max_silence_chunk = 20 # 400 ms of silence
        try:
            while True:
                message = await websocket.receive()

                if message.get("bytes") is not None:
                    chunk = message.get("bytes")

                    if len(chunk) != excpected_chunk_size:
                        await websocket.send_text(f"bad chunk size: {len(chunk)}")
                        continue
                    is_speech = vad.is_speech(chunk, sampleRate)
                    if is_speech:
                        audio_buffer.extend(chunk)
                        silence_chunk = 0
                    else:

                        if len(audio_buffer) > 0:
                            silence_chunk += 1
                            if silence_chunk > max_silence_chunk:
                                audio_data = sr.AudioData(
                                    bytes(audio_buffer),
                                    sample_rate=sampleRate,
                                    sample_width=2
                                )
                                try:
                                    text = recognizer.recognize_google(audio_data, language="he-IL")
                                except sr.UnknownValueError:
                                    text = ""
                                except sr.RequestError:
                                    await websocket.send_text("בעיה בשירות זיהוי הדיבור")
                                    text = ""
                                response = VoiceService.checkTextRequest(text)
                                if response:
                                    await websocket.send_text(response)
                                audio_buffer.clear()
                                text = ""
                                silence_chunk = 0

        except WebSocketDisconnect:
            return
    # need to add the function that changing the voice prefrence in the db
    @staticmethod
    def checkTextRequest(text: str):
        match text:
            case "להחליף קול":
                return "הנה רשימת קולות קול של גבר, אישה, גרוש הנה תגיד אחד מהבחירות ונעשה את זה בישבלך"

            case "אישה":
                return "בחירתך נקלטה נבחר קול של אישה"

            case "גבר":
                return "בחירתך נקלטה נבחר קול של גבר"

            case "גבר גרוש":
                return "בחירה של קול גרוש נבחר"

            case _:
                return None
