import traceback
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dtos.client_dto import ClientInputDTO
from src.application.mappers.client_mapper import ClientMapper
from src.application.use_cases.client_use_case.create_client import CreateClientUseCase
from src.application.use_cases.client_use_case.exceptions_client import (
    ClientNotFoundException,
    EmailAlreadyExistsException,
)
from src.application.use_cases.client_use_case.get_client import GetClientUseCase
from src.infrastructure.database.postgres_client import PostgresConnectionClient
from src.infrastructure.repositories.client_repository import ClientRepository
from src.interfaces.api.v1.exceptions import PostClientException
from src.interfaces.api.v1.schema import ClientRequestSchema, ClientResponseSchema

client_v1_router = APIRouter(prefix="/v1", tags=["Client"])


@client_v1_router.post(
    "/client",
    description="Create a new client",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientResponseSchema,
    response_model_exclude_none=True,
)
async def create_client(
    schema: Annotated[ClientRequestSchema, Body(..., description="Create Client")],
    session: AsyncSession = Depends(PostgresConnectionClient.session),
) -> ClientResponseSchema:
    try:
        client_input_dto = ClientInputDTO(**schema.model_dump())
        client_input_entity = ClientMapper.to_entity(client_input_dto)

        use_case = CreateClientUseCase(
            client_repository=ClientRepository(session),
        )
        client_output_entity = await use_case.execute(client_input_entity)
        return ClientResponseSchema(**client_output_entity.model_dump())
    except EmailAlreadyExistsException as e:
        raise e
    except Exception as e:
        raise PostClientException(
            title="Failed to create client",
            detail={"exception": e.__class__.__name__, "message": str(e)},
            traceback=traceback.format_exc(),
        )


@client_v1_router.get(
    "/client/{client_id}",
    description="Get a client by ID",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponseSchema,
)
async def get_client(
    client_id: Annotated[int, Path(..., description="Client ID")],
    session: AsyncSession = Depends(PostgresConnectionClient.session),
) -> ClientResponseSchema:
    try:
        use_case = GetClientUseCase(
            client_repository=ClientRepository(session),
        )
        client_output_entity = await use_case.execute(client_id)
        return ClientResponseSchema(**client_output_entity.model_dump())
    except ClientNotFoundException as e:
        raise e
    except Exception as e:
        raise PostClientException(
            title="Failed to get client",
            detail={"exception": e.__class__.__name__, "message": str(e)},
            traceback=traceback.format_exc(),
        )
