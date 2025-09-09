from pydantic import BaseModel


class ProductFavoriteSchema(BaseModel):
    price: float
    image: str
    brand: str
    id: int
    title: str
    reviewScore: float


class FavoriteResponseSchema(BaseModel):
    client_id: int
    favorites: list[ProductFavoriteSchema]


class FavoriteRequestSchema(BaseModel):
    product_id: int
