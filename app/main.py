from fastapi import FastAPI
# for CORS
from fastapi.middleware.cors import CORSMiddleware
# SqlAlchemy Local Imports
from . import models
from .database import engine
# Import Routers
from .routers import posts, users, votes, auth



## Using alembic with "--autogenerate" flag we don't need SqlAlchemy
## to auto create tables as we handle it will alembic.'
# Creating all tables defined in models
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# "*" - Means all domains allowed.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World!!!"}
