from abc import ABC, abstractmethod

from pydantic import BaseModel


class ClientRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, item: BaseModel) -> int: ...
