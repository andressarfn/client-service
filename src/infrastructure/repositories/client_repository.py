from dataclasses import dataclass

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from src.infrastructure.models.client_model import ClientModel
from src.infrastructure.repositories.exceptions import (
    EmailAlreadyExistsException,
    NotFoundException,
)


@dataclass(frozen=True)
class ClientRepository(ClientRepositoryInterface):
    session: AsyncSession
    model: type = ClientModel

    async def create(self, item: BaseModel) -> int:
        try:
            stmt = (
                insert(self.model).values(**item.model_dump()).returning(self.model.id)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                logger.error("Email already exists in the database")
                raise EmailAlreadyExistsException(title="Email already exists")

    async def get_by_id(self, id: int) -> BaseModel | None:
        stmt = select(self.model).where(self.model.id == id).limit(1)
        get = await self.session.execute(stmt)
        result = get.scalar_one_or_none()
        if result is None:
            logger.error(f"Client with id {id} not found")
            raise NotFoundException(
                title="client_id not found",
            )
        logger.info(f"Client with id {id} retrieved successfully")
        return result

    async def update(self, id: int, item: BaseModel) -> BaseModel | None:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**item.model_dump(exclude={"created_at"}))
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            client = result.scalar_one_or_none()
            if client is None:
                logger.error(f"Client with id {id} not found for update")
                raise NotFoundException(title="client_id not found")
            logger.info(f"Client with id {id} updated successfully")
            return client
        except IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                logger.error("Email already exists in the database")
                raise EmailAlreadyExistsException(title="Email already exists")

    async def delete(self, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)
        deleted = bool((await self.session.execute(stmt)).rowcount)
        if not deleted:
            logger.error(f"Client with id {id} not found for deletion")
            raise NotFoundException(
                title="client_id not found",
            )
        logger.info(f"Client with id {id} deleted successfully")
