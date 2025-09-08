from dataclasses import dataclass

from src.application.use_cases.client.exceptions import UpdateClientNotFoundException
from src.domain.entities.client_entity import ClientInputEntity, ClientOutputEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from src.infrastructure.repositories.exceptions import NotFoundException


@dataclass(frozen=True)
class UpdateClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(
        self, client_id: int, client_input_entity: ClientInputEntity
    ) -> ClientOutputEntity:
        try:
            client_entity = await self.client_repository.update(
                client_id, client_input_entity
            )
            return ClientOutputEntity(
                client_id=client_entity.id,
                name=client_entity.name,
                email=client_entity.email,
                created_at=str(client_entity.created_at),
                updated_at=str(client_entity.updated_at),
            )
        except NotFoundException:
            raise UpdateClientNotFoundException(
                title="Client not found",
                detail=f"client_id: {client_id} does not exist.",
                status_code=404,
            )
