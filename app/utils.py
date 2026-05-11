from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto") # we are telling passlib to use bcrypt algorithm to hash the password and we are also telling it to automatically detect the deprecated algorithms, it will automatically use the updated algorithms that is up to date 

def hash_password(password: str):
    
    return pwd_context.hash(password)