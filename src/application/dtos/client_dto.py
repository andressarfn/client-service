from pydantic import BaseModel


class ClientInputDTO(BaseModel):
    name: str
    email: str
