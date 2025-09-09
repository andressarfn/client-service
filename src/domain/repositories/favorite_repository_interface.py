from abc import ABC, abstractmethod


class FavoriteRepositoryInterface(ABC):
    @abstractmethod
    async def favorite_exists_for_client(
        self, client_id: int, product_id: str
    ) -> bool: ...

    @abstractmethod
    async def add_favorite(self, client_id: int, favorite_item: str) -> None: ...

    @abstractmethod
    async def get_favorites_by_client_id(self, client_id: int) -> list[str]: ...
