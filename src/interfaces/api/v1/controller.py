from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.client_dto import ClientInputDTO
from src.application.mappers.client_mapper import ClientMapper
from src.application.use_cases.client_use_case.create_client import CreateClientUseCase
from src.infrastructure.database.postgres_client import PostgresConnectionClient
from src.infrastructure.repositories.client_repository import ClientRepository
from src.interfaces.api.v1.schema import ClientRequestSchema, ClientResponseSchema

client_v1_router = APIRouter(prefix="/v1", tags=["Client"])


@client_v1_router.post(
    "/client",
    description="Create a new client",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientResponseSchema,
)
async def create_client(
    schema: Annotated[ClientRequestSchema, Body(..., description="Create Client")],
    session: AsyncSession = Depends(PostgresConnectionClient.session),
) -> ClientResponseSchema:
    client_input_dto = ClientInputDTO(**schema.model_dump())
    client_input_entity = ClientMapper.to_entity(client_input_dto)

    use_case = CreateClientUseCase(
        client_repository=ClientRepository(session),
    )
    client_output_entity = await use_case.execute(client_input_entity)
    return ClientResponseSchema(**client_output_entity.model_dump())
