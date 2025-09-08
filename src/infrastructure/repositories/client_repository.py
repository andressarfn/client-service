from dataclasses import dataclass

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from src.infrastructure.models.client_model import ClientModel
from src.infrastructure.repositories.exceptions import NotFoundException


@dataclass(frozen=True)
class ClientRepository(ClientRepositoryInterface):
    session: AsyncSession

    async def create(self, item: BaseModel) -> int:
        stmt = insert(ClientModel).values(**item.model_dump()).returning(ClientModel.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_by_id(self, id: int) -> BaseModel | None:
        stmt = select(ClientModel).where(ClientModel.id == id).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> None:
        stmt = delete(ClientModel).where(ClientModel.id == id)
        deleted = bool((await self.session.execute(stmt)).rowcount)
        if not deleted:
            logger.error(f"Client with id {id} not found for deletion")
            raise NotFoundException(
                title="client_id not found",
            )
        logger.info(f"Client with id {id} deleted successfully")
