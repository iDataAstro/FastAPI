from pydantic import BaseModel
from typing import Optional
# import yaml
import toml


class PgSettings(BaseModel):
    HOST: str
    PORT: str
    USERNAME: str
    PASSWORD: str
    DATABASE: str


class OAuth2(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class Config(BaseModel):
    APP_NAME: str
    API_HEADER_PASSWORD: Optional[str]
    POSTGRESQL_SETTINGS: PgSettings
    AUTH2_SETTINGS: OAuth2


# with open("app/config.yaml") as config_file:
#     config = Config.parse_obj(yaml.safe_load(config_file))
config = Config.parse_obj(toml.load("config.toml"))
