from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import config

pg_config: dict = config.dict()["POSTGRESQL_SETTINGS"]

# SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@<server-ip>:<port>/<db-name>"
SQLALCHEMY_DATABASE_URL = "postgresql://"+pg_config["USERNAME"]+":"+pg_config["PASSWORD"]+"@"+pg_config["HOST"]+"/"+pg_config["DATABASE"]+""

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()