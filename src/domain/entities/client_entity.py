from pydantic import BaseModel


class ClientInputEntity(BaseModel):
    name: str
    email: str


class ClientOutputEntity(BaseModel):
    client_id: int
