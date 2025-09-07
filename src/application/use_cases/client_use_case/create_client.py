from dataclasses import dataclass

from loguru import logger

from src.domain.entities.client_entity import ClientInputEntity, ClientOutputEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)


@dataclass(frozen=True)
class CreateClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(
        self, client_input_entity: ClientInputEntity
    ) -> ClientOutputEntity:
        logger.info("Creating a new client")
        client_id = await self.client_repository.create(
            item=client_input_entity,
        )

        logger.info(f"Client created with ID: {client_id}")
        return ClientOutputEntity(client_id=client_id)
