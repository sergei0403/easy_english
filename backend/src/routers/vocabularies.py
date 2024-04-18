from fastapi import APIRouter, Depends, Response

from app.dependencies.auth import get_current_user
from app.dependencies.db import DBSessionDep
from schemas.auth_schemas import AuthenticatedUser
from schemas.vocabularies import GetVocabularySchema, CreateVocabularySchema
from services.vocabulary_service import VocabularyDBService


vocabulary_router = APIRouter(prefix="/vocabularies")


@vocabulary_router.get("/user_vocabulary/", response_model=list[GetVocabularySchema])
async def get_user_vocabularis(
    db_session: DBSessionDep, user: AuthenticatedUser = Depends(get_current_user)
):
    vocabulary_service = VocabularyDBService(db_session=db_session)
    query = await vocabulary_service.get_user_vocabularies(user_id=user.id)
    return query


@vocabulary_router.post("/")
async def create_vocabulary(
    item: CreateVocabularySchema,
    db_session: DBSessionDep,
    user: AuthenticatedUser = Depends(get_current_user),
):
    item_dict = item.model_dump()
    item_dict["user_id"] = user.id
    vocabulary_services = VocabularyDBService(db_session=db_session)
    await vocabulary_services.create_vocabulary(item=item_dict)
    return Response(status_code=201)


@vocabulary_router.patch("/{vocabulary_id}/")
async def update_vocabulary(
    vocabulary_id: int,
    item: CreateVocabularySchema,
    db_session: DBSessionDep,
    user: AuthenticatedUser = Depends(get_current_user),
):
    vocabulary_service = VocabularyDBService(db_session=db_session)
    await vocabulary_service.update_vocabulary(item=item, vocabulary_id=vocabulary_id)
    return Response(status_code=204)


@vocabulary_router.delete("/{vocabulary_id}/")
async def delete_vocabulary(
    vocabulary_id: int,
    db_session: DBSessionDep,
    user: AuthenticatedUser = Depends(get_current_user),
):
    vocabulary_service = VocabularyDBService(db_session=db_session)
    await vocabulary_service.delete_vocabularies_by_id(id=vocabulary_id)
    return Response(status_code=201)
