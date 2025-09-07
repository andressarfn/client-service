from dataclasses import dataclass

from pydantic import BaseModel
from sqlalchemy import insert
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
