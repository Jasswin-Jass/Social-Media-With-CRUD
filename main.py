from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

from sentry_sdk import HttpTransport

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish:  bool = True
    rating: Optional[int] = None

my_posts = [{"title": "ONE", "content": "This is post one dude", "id": 1}, {"title": "TWO", "content": "Second one here", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
                return p

@app.get("/")
def root():
    return {"message": "Hello jass"} 

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    print(new_post) # new_post here is in pydantic model(data type) which has attributes that we mentiond in the base model class
    print(new_post.model_dump()) # to convert a pydatic model to a dictionary use .model_dump() method and you can use model_dump_json() for json

    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id :int, respose: Response):
    post = find_post(id)
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"post with id {id} was not found")
        # respose.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}     You can also use this instead 
    return {"post data": post}
        
