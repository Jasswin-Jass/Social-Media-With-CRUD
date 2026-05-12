from fastapi import Depends, FastAPI, Response, status, HTTPException 
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models, schemas, utils
from .database import engine , get_db
from sqlalchemy.orm import Session
from .routers import post, user

models.Base.metadata.create_all(bind=engine)   # this will create the tables in the database based on the models we have defined in the models.py file. We can just run this code once and it will create the tables for us. We don't need to run this code every time we start the server. We can just comment it out after running it once.

app = FastAPI()


# while (True):
     

#     try: 
#         conn = psycopg2.connect(
#             host='localhost', 
#             database='Fastapi', 
#             user='postgres', 
#             password='jass@@00', 
#             cursor_factory=RealDictCursor    # we use this to get the column names in the output instead of just getting the values in a list and it is imported from psycopg2.extras
#             )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Cennection to database failed")
#         print("Error:", error)
#         time.sleep(2)

my_posts = [{"title": "ONE", "content": "This is post one dude", "id": 1}, {"title": "TWO", "content": "Second one here", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
                return p

def find_index(id):
     for i, p in enumerate(my_posts):
          if p['id'] == id:
               return i


app.include_router(post.router) # this will include the routes from the post router in the main app and we can use the routes defined in the post router in our main app and also we can use the routes defined in the post router in other routers if we want to and it is a good practice to use routers.
app.include_router(user.router) # same with useer router


@app.get("/")
def root():
    return {"message": "Hello jass"} 