from .. import models, schemas, utils
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = utils.hash_password(user.password) # the function to hash passwords is in the utils.py file and we are importing and using it  

    new_user = models.User(**user.model_dump()) # this will create a new post object based on the data that we have in the post object that we get from the request body and it will also convert the post object to a dictionary and then we can use the values of that dictionary to create a new post object and we can also use the model_dump() method to get the data from the post object in a dictionary format and then we use ** to unpack the dict and pass as eg. id=post.id 
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # this will refresh the new_post object with the data from the database and it will also get the id of the new post that was created in the database and it is important to do this after committing the changes to the database because before committing, the new_post object will not have an id and it will be None and after committing, it will have an id and we can use that id to return the new post in the response.
    
    return new_user

@router.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends((get_db))):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"The user of id {id} is not found")
    return user