from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#note: We need SECRET_KEY, ALGORITHM, and EXPIRATION_TIME

SECRET_KEY = "asdf0987;lkj1234qwer0987poiu1234zcxv0987,mnb1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy() # we create a copy of the data dict so that we can modify it without affecting the original data dict
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # we calcutate the expiration time for the token by adding the current time with the expiration time in minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception): # this is to verify the acces tokens

    try: 
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        id: Optional[int] = payload.get("user_id") # we get the user_id from the payload of the token and we use Optional[str] because it can be None if there is no user_id in the payload and we also specify that it is a string because the user_id is a string in our case but it can be an int or any other type depending on how you set it up in your application
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)): 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authernticate": "Bearer"})

    return verify_access_token(token=token, credentials_exception=credentials_exception)
