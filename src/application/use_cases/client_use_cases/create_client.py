from dataclasses import dataclass

from loguru import logger
from src.application.use_cases.client_use_cases.exceptions_client import (
    CreateClientEmailAlreadyExistsException,
)
from src.domain.entities.client_entity import ClientInputEntity, ClientOutputEntity
from src.domain.repositories.client_repository_interface import (
    ClientRepositoryInterface,
)
from sqlalchemy.exc import IntegrityError


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
        except Exception as e:
            if isinstance(
                e, IntegrityError
            ) and "duplicate key value violates unique constraint " in str(e.orig):
                raise CreateClientEmailAlreadyExistsException(
                    title="Email already exists",
                    detail="A client with this email already exists.",
                    status_code=400,
                )
            raise e
