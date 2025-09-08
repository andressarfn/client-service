from dataclasses import dataclass

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from src.infrastructure.models.client_model import ClientModel


@dataclass(frozen=True)
class ClientRepository(ClientRepositoryInterface):
    session: AsyncSession

    async def create(self, item: BaseModel) -> int:
        stmt = insert(ClientModel).values(**item.model_dump()).returning(ClientModel.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_by_key(self, key: int | str) -> ClientModel | None:
        if isinstance(key, int):
            stmt = select(ClientModel).where(ClientModel.id == key).limit(1)
        elif isinstance(key, str):
            stmt = select(ClientModel).where(ClientModel.email == key).limit(1)
        else:
            raise ValueError("Key must be int (id) or str (email)")
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
