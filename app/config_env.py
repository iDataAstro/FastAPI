from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str
    API_HEADER_PASSWORD: Optional[str]
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: str
    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str
    AUTH2_SECRET_KEY: str
    AUTH2_ALGORITHM: str
    AUTH2_ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".local_env_file"


# To use BaseSettings import this file and access the settings as below.
# settings = Settings()
# print(settings.POSTGRESQL_HOST)
