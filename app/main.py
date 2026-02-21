from traceback import print_tb

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

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

def find_index(id):
     for i, p in enumerate(my_posts):
          if p['id'] == id:
               return i

@app.get("/")
def root():
    return {"message": "Hello jass"} 

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
        
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
     # deleting a post
     index = find_index(id)
     
     if index == None:
          raise HTTPException(status_code=404, detail=f"The post of id {id} is not found")

     my_posts.pop(index) 
     return Response(status_code=status.HTTP_204_NO_CONTENT) # if you send a response of 204, you shouldn't be sending any message back

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
     index = find_index(id)
     
     if index == None:
          raise HTTPException(status_code=404, detail=f"The post of id {id} is not found")
     post_dict = post.model_dump()
     post_dict['id'] = id
     my_posts[index] = post_dict
     return {'data': post_dict }
     
