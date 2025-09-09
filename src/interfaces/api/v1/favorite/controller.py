import traceback
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.favorite.add import AddFavoriteUseCase
from src.application.use_cases.favorite.exceptions import (
    FavoriteProductAlreadyExistsError,
    FavoriteProductNotFoundError,
)
from src.application.use_cases.favorite.get import GetFavoriteUseCase
from src.infrastructure.database.postgres_client import PostgresConnectionClient
from src.infrastructure.external_services.products.product_client import (
    ProductClientInterface,
)
from src.infrastructure.repositories.favorite_repository import FavoriteRepository
from src.interfaces.api.v1.favorite.dependencies import get_product_client
from src.interfaces.api.v1.favorite.exceptions import (
    GetFavoriteException,
    PostFavoriteException,
)
from src.interfaces.api.v1.favorite.schema import (
    FavoriteRequestSchema,
    FavoriteResponseSchema,
)

favorite_v1_router = APIRouter(prefix="/v1", tags=["Favorite"])


@favorite_v1_router.post(
    "/client/{client_id}/favorite",
    description="Add a favorite item for a client",
    status_code=status.HTTP_201_CREATED,
    response_model=FavoriteResponseSchema,
)
async def add_favorite(
    client_id: Annotated[int, Path(..., description="Client ID")],
    favorite_item: Annotated[
        FavoriteRequestSchema, Body(..., description="Favorite Item")
    ],
    session: Annotated[AsyncSession, Depends(PostgresConnectionClient.session)],
    product_client: Annotated[ProductClientInterface, Depends(get_product_client)],
):
    try:
        use_case = AddFavoriteUseCase(
            favorite_repository=FavoriteRepository(session),
            product_client=product_client,
        )
        result = await use_case.execute(client_id, favorite_item.product_id)
        return FavoriteResponseSchema(id=result)
    except (FavoriteProductNotFoundError, FavoriteProductAlreadyExistsError) as e:
        raise e
    except Exception as e:
        raise PostFavoriteException(
            title="Failed to add favorite",
            detail={"exception": e.__class__.__name__, "message": str(e)},
            traceback=traceback.format_exc(),
        )


@favorite_v1_router.get(
    "/client/{client_id}/favorites",
    description="Get all favorite items for a client",
    status_code=status.HTTP_200_OK,
    response_model=FavoriteResponseSchema,
)
async def get_favorites(
    client_id: Annotated[int, Path(..., description="Client ID")],
    session: Annotated[AsyncSession, Depends(PostgresConnectionClient.session)],
    product_client: Annotated[ProductClientInterface, Depends(get_product_client)],
):
    try:
        use_case = GetFavoriteUseCase(
            favorite_repository=FavoriteRepository(session),
            product_client=product_client,
        )
        favorites = await use_case.execute(client_id)
        return FavoriteResponseSchema(
            **favorites.model_dump(),
        )
    except Exception as e:
        raise GetFavoriteException(
            title="Failed to get favorites",
            detail={"exception": e.__class__.__name__, "message": str(e)},
            traceback=traceback.format_exc(),
        )
