from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#note: We need SECRET_KEY, ALGORITHM, and EXPIRATION_TIME

SECRET_KEY = "asdf0987;lkj1234qwer0987poiu1234zcxv0987,mnb1234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy() # we create a copy of the data dict so that we can modify it without affecting the original data dict
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # we calcutate the expiration time for the token by adding the current time with the expiration time in minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try: 
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        id: Optional[str] = payload.get("user_id") # this is to verify the acces tokens
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme)): 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authernticate": "Bearer"})

    return verify_access_token(token=token, credentials_exception=credentials_exception)
