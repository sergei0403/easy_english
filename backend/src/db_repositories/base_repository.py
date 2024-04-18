from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=Base)


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class BaseDBRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.__db_session = db_session

    def get_db(self):
        return self.__db_session

    async def get(self, *, id: Union[UUID, int]) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        response = await self.__db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: List[Union[UUID, str]],
    ) -> Optional[List[ModelType]]:
        response = await self.__db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = await self.__db_session.execute(query)
        return response.scalars().all()

    async def execute_query(self, *, query: Optional[Union[T]] = None) -> Any:
        response = await self.__db_session.execute(query)
        return response.fetchall()

    async def get_multi_paginated(
        self, *, params: Optional[Params] = Params(), query: Optional[Union[T]] = None
    ) -> Page[ModelType]:
        if query is None:
            query = select(self.model)
        return await paginate(self.__db_session, query, params)

    async def get_multi_paginated_ordered(
        self,
        *,
        params: Optional[Params] = Params(),
        order_by: Optional[str] = None,
        order: Optional[IOrderEnum] = IOrderEnum.ascendent,
        query: Optional[Union[T]] = None,
    ) -> Page[ModelType]:
        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = self.model.id

        if query is None:
            if order == IOrderEnum.ascendent:
                query = select(self.model).order_by(columns[order_by].asc())
            else:
                query = select(self.model).order_by(columns[order_by].desc())

        return await paginate(self.__db_session, query, params)

    async def get_multi_ordered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order: Optional[IOrderEnum] = IOrderEnum.ascendent,
    ) -> List[ModelType]:
        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = self.model.id

        if order == IOrderEnum.ascendent:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by].asc())
            )
        else:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by].desc())
            )

        response = await self.__db_session.execute(query)
        return response.scalars().all()

    async def create(self, obj_in: Union[Dict[str, Any]]) -> ModelType:
        db_obj = self.model(**obj_in)
        try:
            self.__db_session.add(db_obj)
            await self.__db_session.flush()
            await self.__db_session.commit()
        except exc.IntegrityError as e:
            print(e)
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: Union[Dict[str, Any], ModelType],
    ) -> ModelType:
        obj_data = jsonable_encoder(obj_current)
        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])

        self.__db_session.add(obj_current)
        await self.__db_session.flush()
        await self.__db_session.commit()
        await self.__db_session.refresh(obj_current)
        return obj_current

    async def update_by_id(
        self,
        *,
        id: Union[UUID, str],
        obj_in: Union[Dict[str, Any], ModelType],
    ) -> ModelType:
        self.__db_session = self.__db_session or self.db.session
        obj = await self.get(id=id)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail="Resource not found",
            )
        return await self.update(obj_current=obj, obj_new=obj_in)

    async def remove(self, *, id: Union[UUID, str]) -> ModelType:
        response = await self.__db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = response.scalar_one()
        await self.__db_session.delete(obj)
        await self.__db_session.flush()
        await self.__db_session.commit()
        return obj
