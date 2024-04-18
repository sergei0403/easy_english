from pydantic import BaseModel


class GetUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CreateVocabularySchema(BaseModel):
    name: str


class FullCreateVocabularySchema(BaseModel):
    name: str
    user_id: int


class GetVocabularySchema(BaseModel):
    id: int
    name: str
    user: GetUser

    class Config:
        from_attributes = True
