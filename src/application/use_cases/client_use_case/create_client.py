from dataclasses import dataclass

from loguru import logger

from src.application.use_cases.client_use_case.exceptions_client import (
    EmailAlreadyExistsException,
)
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

        logger.info("Checking if email already exists")
        existing_client = await self.client_repository.get_by_key(
            client_input_entity.email,
        )
        if existing_client:
            logger.error(f"Email {client_input_entity.email} already exists")
            raise EmailAlreadyExistsException(
                title="Email already exists",
                detail=f"Email {client_input_entity.email} is already in use.",
                status_code=400,
            )

        logger.info("Creating a new client")
        client_id = await self.client_repository.create(
            item=client_input_entity,
        )

        logger.info(f"Client created with ID: {client_id}")
        return ClientOutputEntity(client_id=client_id)
