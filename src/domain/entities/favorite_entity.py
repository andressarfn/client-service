from pydantic import BaseModel


class ProductFavoriteEntity(BaseModel):
    price: float
    image: str
    brand: str
    id: int
    title: str
    reviewScore: float


class FavoriteResponseEntity(BaseModel):
    client_id: int
    favorites: list[ProductFavoriteEntity]
