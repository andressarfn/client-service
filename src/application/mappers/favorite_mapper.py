from src.application.dtos.favorite_dto import FavoriteInputDTO
from src.domain.entities.favorite_entity import FavoriteInputEntity


class FavoriteMapper:
    @staticmethod
    def to_entity(dto: FavoriteInputDTO) -> FavoriteInputEntity:
        return FavoriteInputEntity(client_id=dto.client_id, product_id=dto.product_id)
