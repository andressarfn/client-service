from dataclasses import dataclass

from src.application.use_cases.client.exceptions import (
    GetClientNotFoundException,
)
from src.domain.entities.client_entity import ClientInputEntity, ClientOutputEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from src.infrastructure.repositories.exceptions import NotFoundException


@dataclass(frozen=True)
class GetClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(self, client_id: int) -> ClientInputEntity:
        try:
            client_entity = await self.client_repository.get_by_id(client_id)
            return ClientOutputEntity(
                client_id=client_entity.id,
                name=client_entity.name,
                email=client_entity.email,
                created_at=str(client_entity.created_at),
                updated_at=str(client_entity.updated_at),
            )
        except NotFoundException:
            raise GetClientNotFoundException(
                title="client_id not found",
                detail=f"client_id: {client_id} does not exist.",
                status_code=404,
            )
