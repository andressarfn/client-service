from pydantic import BaseModel, EmailStr


class ClientRequestSchema(BaseModel):
    name: str
    email: EmailStr


class ClientResponseSchema(BaseModel):
    client_id: int
    name: str | None = None
    email: EmailStr | None = None
    created_at: str | None = None
