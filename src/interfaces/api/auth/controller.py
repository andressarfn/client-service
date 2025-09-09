from typing import Annotated
from fastapi import APIRouter, Body

from fastapi import status
from jose import jwt
from passlib.hash import bcrypt

from src.interfaces.api.auth.exceptions import AuthenticationException
from src.interfaces.api.auth.schemas import LoginRequest, TokenResponse

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

# Fake user for demonstration
fake_user = {
    "email": "user@example.com",
    "hashed_password": bcrypt.hash("senha123"),
    "user_id": 1,
}


@auth_router.post(
    "/login",
    description="User login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
async def login(
    data: Annotated[LoginRequest, Body(..., description="Login Data")],
) -> TokenResponse:
    if data.email != fake_user["email"] or not bcrypt.verify(
        data.password, fake_user["hashed_password"]
    ):
        raise AuthenticationException(
            title="Invalid credentials",
            detail="The provided email or password is incorrect.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = jwt.encode(
        {"sub": str(fake_user["user_id"])}, SECRET_KEY, algorithm=ALGORITHM
    )
    return TokenResponse(access_token=token, expires_in=3600)
