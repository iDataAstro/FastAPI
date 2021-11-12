from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fast_api_demo',
                                user='postgres',
                                password='fastapi',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established!!")
        break
    except Exception as error:
        print("Database connection FAILED!!!")
        print("Error: ", error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/posts/{id}")
# Method 1 for error messaging
# def get_posts(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         # response.status_code = 404
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"Post not found with id:{id}"}
#     return {"post_detail": f"Here is post {post}"}
# Method 2 for error messages - MUCH CLEANER WAY
def get_posts(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id:{id}")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id:{id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post_detail(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    update_post = cursor.fetchone()
    conn.commit()
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id:{id}")

    return {"update_post_detail": update_post}
