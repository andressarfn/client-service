from pydantic import BaseModel


class ClientInputEntity(BaseModel):
    name: str
    email: str


class ClientOutputEntity(BaseModel):
    client_id: int
    name: str | None = None
    email: str | None = None
    created_at: str | None = None
