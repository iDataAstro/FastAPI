from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# SqlAlchemy Imports
from sqlalchemy.orm import Session
# SqlAlchemy Local Imports
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(tags=["Authentication"])

# OAuth2PasswordRequestForm contains {"username":"username", "password":"password"}


@router.post("/login", response_model=schemas.Token)
def login(user_auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_auth.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username or password!!")

    if not utils.verify_password(user_auth.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username or password!!")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
