from dataclasses import dataclass

from src.application.use_cases.client.exceptions import (
    ClientNotFoundException,
)
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from src.infrastructure.repositories.exceptions import NotFoundException


@dataclass(frozen=True)
class DeleteClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(self, client_id: int) -> None:
        try:
            await self.client_repository.delete(client_id)
        except NotFoundException:
            raise ClientNotFoundException(
                title="client_id not found",
                detail=f"client_id: {client_id} does not exist.",
                status_code=404,
            )
