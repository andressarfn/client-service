import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Product Service"
    DESCRIPTION: str = "Study Project"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    ROOT_PATH: str = "client-service"

    DATABASE_URL: str = ""
    DATABASE_SCHEMA: str = ""

    class Config:
        env_file = "ENV_FILE" if "ENV_FILE" in os.environ else ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
