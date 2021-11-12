from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
# SqlAlchemy Imports
from sqlalchemy.orm import Session
# SqlAlchemy Local Imports
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id:{id}")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_id = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id:{id}")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post_detail(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db),
                       user_id: int = Depends(oauth2.get_current_user)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.update(post.dict(), synchronize_session=False)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id:{id}")
    db.commit()
    return update_query.first()
