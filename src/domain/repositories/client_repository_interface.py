from abc import ABC, abstractmethod

from pydantic import BaseModel


class ClientRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, item: BaseModel) -> int: ...

    @abstractmethod
    async def get_by_key(self, key: int | str) -> BaseModel | None: ...
