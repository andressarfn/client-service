from pydantic import BaseModel


class ProductFavoriteEntity(BaseModel):
    price: float
    image: str
    brand: str
    id: int
    title: str
    reviewScore: float


class FavoriteInputEntity(BaseModel):
    client_id: int
    product_id: int | None = None


class FavoritesOutputEntity(BaseModel):
    client_id: int
    favorites: list[ProductFavoriteEntity]


class FavoriteOutputEntity(BaseModel):
    product_id: int
    message: str = "Favorite item added successfully"
