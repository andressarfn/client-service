from dataclasses import dataclass

from loguru import logger
from src.application.use_cases.client.exceptions import (
    CreateClientEmailAlreadyExistsException,
)
from src.domain.entities.client_entity import ClientInputEntity, ClientOutputEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)

from src.infrastructure.repositories.exceptions import EmailAlreadyExistsException


@dataclass(frozen=True)
class CreateClientUseCase:
    client_repository: ClientRepositoryInterface

    async def execute(
        self, client_input_entity: ClientInputEntity
    ) -> ClientOutputEntity:
        try:
            logger.info("Creating a new client")
            client_id = await self.client_repository.create(
                item=client_input_entity,
            )

            logger.info(f"Client created with ID: {client_id}")
            return ClientOutputEntity(client_id=client_id)
        except EmailAlreadyExistsException as e:
            raise CreateClientEmailAlreadyExistsException(
                title=e.title,
                detail="The email provided is already in use.",
                status_code=400,
            )
