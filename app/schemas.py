from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True) # just use this line so pydantic can read the data from the database and convert it to a pydantic model and this is important because when we get the data from the database it will be in the form of an object and we need to convert it to a pydantic model so that we can return it in the response and also we can use this line to convert the data from the database to a pydantic model and then we can use that model to return the data in the response.
    #we can also skip this line cuz modern pydantic 2 can read this without the above line but it is a better practice to use it and ot avoid future errors 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int] = None

