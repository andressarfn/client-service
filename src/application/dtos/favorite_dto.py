from pydantic import BaseModel


class FavoriteInputDTO(BaseModel):
    client_id: int
    product_id: int
