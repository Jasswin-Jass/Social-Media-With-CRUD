from fastapi import Depends, FastAPI, Response, status, HTTPException 
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models
from .database import engine , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)   # this will create the tables in the database based on the models we have defined in the models.py file. We can just run this code once and it will create the tables for us. We don't need to run this code every time we start the server. We can just comment it out after running it once.

app = FastAPI()

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
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    
    new_post = models.Post(**post.model_dump()) # this will create a new post object based on the data that we have in the post object that we get from the request body and it will also convert the post object to a dictionary and then we can use the values of that dictionary to create a new post object and we can also use the model_dump() method to get the data from the post object in a dictionary format and then we use ** to unpack the dict and pass as eg. id=post.id 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # this will refresh the new_post object with the data from the database and it will also get the id of the new post that was created in the database and it is important to do this after committing the changes to the database because before committing, the new_post object will not have an id and it will be None and after committing, it will have an id and we can use that id to return the new post in the response.
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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

