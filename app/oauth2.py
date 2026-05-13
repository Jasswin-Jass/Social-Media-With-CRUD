from asyncio.constants import ACCEPT_RETRY_DELAY
from ssl import AlertDescription

from jose import JWTError, jwt
from datetime import datetime, timedelta

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