from dataclasses import dataclass

from src.application.use_cases.client_use_cases.exceptions_client import (
    GetClientNotFoundException,
)
from src.domain.entities.client_entity import ClientInputEntity, ClientOutputEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)


@dataclass(frozen=True)
class GetClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(self, client_id: int) -> ClientInputEntity:
        client_entity = await self.client_repository.get_by_id(client_id)
        if client_entity is None:
            raise GetClientNotFoundException(
                title="client_id not found",
                detail=f"client_id: {client_id} does not exist.",
                status_code=404,
            )

        return ClientOutputEntity(
            client_id=client_entity.id,
            name=client_entity.name,
            email=client_entity.email,
            created_at=str(client_entity.created_at),
        )
