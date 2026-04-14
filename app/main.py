from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published:  bool = True

while (True):
     

    try: 
        conn = psycopg2.connect(
            host='localhost', 
            database='Fastapi', 
            user='postgres', 
            password='jass@@00', 
            cursor_factory=RealDictCursor    # we use this to get the column names in the output instead of just getting the values in a list and it is imported from psycopg2.extras
            )
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Cennection to database failed")
        print("Error:", error)
        time.sleep(2)

my_posts = [{"title": "ONE", "content": "This is post one dude", "id": 1}, {"title": "TWO", "content": "Second one here", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
                return p

def find_index(id):
     for i, p in enumerate(my_posts):
          if p['id'] == id:
               return i

@app.get("/")
def root():
    return {"message": "Hello jass"} 

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()
    
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id :int, respose: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = find_post(id)
    post =cursor.fetchone()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
        # respose.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}     You can also use this instead 
    return {"post data": post}
        
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting a post
    #index = find_index(id)
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    index = cursor.fetchone()
    conn.commit()
    
    if index == None:
        raise HTTPException(status_code=404, detail=f"The post of id {id} is not found")
    
    #my_posts.pop(index) 
    return Response(status_code=status.HTTP_204_NO_CONTENT) # if you send a response of 204, you shouldn't be sending any message back

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    #index = find_index(id)
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"The post of id {id} is not found")
    
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    return {'data': updated_post }
     
