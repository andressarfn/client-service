from dataclasses import dataclass

from loguru import logger

from src.application.use_cases.favorite.exceptions import (
    FavoriteProductAlreadyExistsError,
    FavoriteProductNotFoundError,
)
from src.domain.entities.favorite_entity import (
    FavoriteInputEntity,
    FavoriteOutputEntity,
)
from src.domain.repositories.favorite_repository_interface import (
    FavoriteRepositoryInterface,
)
from src.infrastructure.external_services.products.product_client import (
    ProductClientInterface,
)


@dataclass(frozen=True)
class AddFavoriteUseCase:
    favorite_repository: FavoriteRepositoryInterface
    product_client: ProductClientInterface

    async def execute(self, favorite_entity: FavoriteInputEntity) -> int:
        logger.info(
            f"Adding favorite item for client_id: {favorite_entity.client_id}, product_id: {favorite_entity.product_id}"
        )
        if not await self._check_product_exists(favorite_entity.product_id):
            logger.error(f"Product with id {favorite_entity.product_id} not found.")
            raise FavoriteProductNotFoundError(
                title="Product not found",
                detail=f"Product with id {favorite_entity.product_id} not found.",
                status_code=400,
            )
        if await self._check_favorite_exists(
            favorite_entity.client_id, favorite_entity.product_id
        ):
            logger.error(
                f"Favorite item with product_id: {favorite_entity.product_id} already exists "
                f"for client_id: {favorite_entity.client_id}"
            )
            raise FavoriteProductAlreadyExistsError(
                title="Favorite already exists",
                detail=f"Favorite item with product_id: {favorite_entity.product_id} already exists "
                f"for client_id: {favorite_entity.client_id}",
                status_code=400,
            )

        result = await self.favorite_repository.add_favorite(
            favorite_entity.client_id, favorite_entity.product_id
        )
        logger.info(
            f"Favorite product_id: {favorite_entity.product_id} added for client_id: "
            f"{favorite_entity.client_id}, item_id: {result}"
        )
        return FavoriteOutputEntity(product_id=favorite_entity.product_id)

    async def _check_product_exists(self, product_id: int) -> bool:
        return await self.product_client.get_product_by_id(product_id) is not None

    async def _check_favorite_exists(self, client_id: int, product_id: int) -> bool:
        return await self.favorite_repository.favorite_exists_for_client(
            client_id, product_id
        )
