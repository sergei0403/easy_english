from pydantic import BaseModel

class GetVocabulary(BaseModel):
    id: int
    name: str
    user_id: int