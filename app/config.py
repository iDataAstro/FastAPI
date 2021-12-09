import os

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
if os.environ.get("CURRENT_ENV", "DEV") != "DEV":
    cfgtoml = {}

    cfgtoml["APP_NAME"] = os.environ["APP_NAME"]
    cfgtoml["API_HEADER_PASSWORD"] = os.environ["API_HEADER_PASSWORD"]

    cfgtoml["POSTGRESQL_SETTINGS"] = {}
    cfgtoml["POSTGRESQL_SETTINGS"]["HOST"] = os.environ["POSTGRESQL_SETTINGS_HOST"]
    cfgtoml["POSTGRESQL_SETTINGS"]["PORT"] = os.environ["POSTGRESQL_SETTINGS_PORT"]
    cfgtoml["POSTGRESQL_SETTINGS"]["USERNAME"] = os.environ["POSTGRESQL_SETTINGS_USERNAME"]
    cfgtoml["POSTGRESQL_SETTINGS"]["PASSWORD"] = os.environ["POSTGRESQL_SETTINGS_PASSWORD"]
    cfgtoml["POSTGRESQL_SETTINGS"]["DATABASE"] = os.environ["POSTGRESQL_SETTINGS_DATABASE"]

    cfgtoml["AUTH2_SETTINGS"] = {}
    cfgtoml["AUTH2_SETTINGS"]["SECRET_KEY"] = os.environ["AUTH2_SETTINGS_SECRET_KEY"]
    cfgtoml["AUTH2_SETTINGS"]["ALGORITHM"] = os.environ["AUTH2_SETTINGS_ALGORITHM"]
    cfgtoml["AUTH2_SETTINGS"]["ACCESS_TOKEN_EXPIRE_MINUTES"] = os.environ["AUTH2_SETTINGS_ACCESS_TOKEN_EXPIRE_MINUTES"]

    config_file = f"config_{os.environ['CURRENT_ENV']}.toml"
    with open(config_file, "w") as f:
        toml.dump(cfgtoml, f)
    config = Config.parse_obj(toml.load(config_file))
