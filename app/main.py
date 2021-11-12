from fastapi import FastAPI
# SqlAlchemy Local Imports
from . import models
from .database import engine
# Import Routers
from .routers import posts, users, auth


# Creating all tables defined in models
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
