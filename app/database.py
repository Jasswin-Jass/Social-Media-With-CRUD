from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:jass%40%4000@localhost/Fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): # this is a function that will create a new database session for each request and then close it after the request is done. We can use this function as a dependency in our routes to get a database session.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

""" All the above code is for setting up the database connection and create a session to interact with the database and also to create a base class for our models to inherit from.
we can just copy and paste this code for other projects and just change the database and stuff and it will work fine. """

