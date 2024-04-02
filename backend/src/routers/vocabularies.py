from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import joinedload

from app.dependencies.auth import get_current_user
from app.dependencies.db import DBSessionDep
from models import Vocabulary
from schemas.auth_schemas import AuthenticatedUser


class GetUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CreateVocabularySchema(BaseModel):
    name: str


class GetVocabularySchema(BaseModel):
    id: int
    name: str
    user: GetUser

    class Config:
        from_attributes = True


vocabulary_router = APIRouter(prefix="/vocabularies")


@vocabulary_router.get("/user_vocabulary/", response_model=list[GetVocabularySchema])
async def get_user_vocabularis(
    db_session: DBSessionDep, user: AuthenticatedUser = Depends(get_current_user)
):
    query = await db_session.execute(
        select(Vocabulary)
        .where(Vocabulary.user_id == user.id)
        .options(joinedload(Vocabulary.user))
    )
    return query.scalars().all()


@vocabulary_router.get("/", response_model=list[GetVocabularySchema])
async def get_vocabularis(
    db_session: DBSessionDep, user: AuthenticatedUser = Depends(get_current_user)
):
    query = await db_session.execute(
        select(Vocabulary).options(joinedload(Vocabulary.user))
    )
    return query.scalars().all()


@vocabulary_router.post("/")
async def create_vocabulary(
    item: CreateVocabularySchema,
    db_session: DBSessionDep,
    user: AuthenticatedUser = Depends(get_current_user),
):
    item_dict = item.dict()
    item_dict["user_id"] = user.id
    await db_session.execute(
        insert(Vocabulary).values(
            name=item_dict.get("name"), user_id=item_dict.get("user_id")
        )
    )
    await db_session.commit()
    return Response(status_code=201)


@vocabulary_router.patch("/{vocabulary_id}/")
async def update_vocabulary(
    vocabulary_id: int,
    item: CreateVocabularySchema,
    db_session: DBSessionDep,
    user: AuthenticatedUser = Depends(get_current_user),
):
    existing_vocabulary = await db_session.execute(
        select(Vocabulary).where(Vocabulary.id == vocabulary_id)
    )
    if existing_vocabulary is None:
        return Response(status_code=404, content="Vocabulary not found")

    # Update the vocabulary item with the new data
    await db_session.execute(
        update(Vocabulary).where(Vocabulary.id == vocabulary_id).values(name=item.name)
    )
    await db_session.commit()
    return Response(status_code=204)


@vocabulary_router.delete("/{vocabulary_id}/")
async def delete_vocabulary(
    vocabulary_id: int,
    db_session: DBSessionDep,
    user: AuthenticatedUser = Depends(get_current_user),
):
    existing_vocabulary = await db_session.execute(
        delete(Vocabulary).where(
            Vocabulary.id == vocabulary_id, Vocabulary.user_id == user.id
        )
    )
    if existing_vocabulary is None:
        return Response(status_code=404, content="Vocabulary not found")
    return Response(status_code=201)
