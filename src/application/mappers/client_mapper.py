from src.application.dtos.client_dto import ClientInputDTO
from src.domain.entities.client_entity import ClientInputEntity


class ClientMapper:
    @staticmethod
    def to_entity(dto: ClientInputDTO) -> ClientInputEntity:
        return ClientInputEntity(**dto.model_dump())
