from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.favorite_repository_interface import (
    FavoriteRepositoryInterface,
)
from src.infrastructure.models.favorite_model import FavoriteModel


@dataclass(frozen=True)
class FavoriteRepository(FavoriteRepositoryInterface):
    session: AsyncSession
    model: type = FavoriteModel

    async def favorite_exists_for_client(self, client_id: int, product_id: str) -> bool:
        stmt = select(self.model).where(
            self.model.client_id == client_id,
            self.model.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_favorite(self, client_id: int, product_id: str) -> int | None:
        stmt = (
            insert(self.model)
            .values(client_id=client_id, product_id=product_id)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_favorites_by_client_id(self, client_id: int) -> list[int]:
        stmt = (
            select(self.model.product_id)
            .where(self.model.client_id == client_id)
            .order_by(self.model.added_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
