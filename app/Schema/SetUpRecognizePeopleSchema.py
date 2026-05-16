from pydantic import BaseModel

class SetUpRecognizePeopleSchema(BaseModel):
    name: str
    where_is_known_from: str