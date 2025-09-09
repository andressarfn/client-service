from dataclasses import dataclass

from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)


@dataclass(frozen=True)
class DeleteClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(self, client_id: int) -> None:
        await self.client_repository.delete(client_id)
