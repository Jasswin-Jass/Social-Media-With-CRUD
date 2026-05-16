# POST CRUD OPERATIONS

from .. import models, schemas, oauth2
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"] 
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # the response model is used to specify the model we want to give the response, it is in the schemas file
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # type: ignore # this will create a new post object based on the data that we have in the post object that we get from the request body and it will also convert the post object to a dictionary and then we can use the values of that dictionary to create a new post object and we can also use the model_dump() method to get the data from the post object in a dictionary format and then we use ** to unpack the dict and pass as eg. id=post.id 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # this will refresh the new_post object with the data from the database and it will also get the id of the new post that was created in the database and it is important to do this after committing the changes to the database because before committing, the new_post object will not have an id and it will be None and after committing, it will have an id and we can use that id to return the new post in the response.
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id :int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # #post = find_post(id)
    # post =cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first() # this will filter the posts based on the id and it will return the first post that matches the id and if there is no post that matches it will return None 

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
        # respose.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}     You can also use this instead 
    return post
        
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting a post
    #index = find_index(id)
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # index = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    user_post = post_query.first() # this will get the first post that matches the id and if there is no post that matches it will return None
    
    if user_post is None:
        raise HTTPException(status_code=404, detail=f"The post of id {id} is not found")
    
    if user_post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        

    #my_posts.pop(index) 

    post_query.delete(synchronize_session=False) # this will delete the post from the database and it will also synchronize the session with the database and it is important to do this because if we don't do this, then the session will not be aware of the changes that we have made to the database and it will not be able to commit those changes to the database and it will also cause issues when we try to query the database after deleting a post because the session will still think that the post is there and it will return an error when we try to query for that post after deleting it.
    db.commit() # this will commit the changes to the database and it is important to do this after deleting a post because if we don't do this, then the changes that we have made to the database will not be saved 
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) # if you send a response of 204, you shouldn't be sending any message back

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #index = find_index(id)
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    user_post = post_query.first()

    if user_post == None:
        raise HTTPException(status_code=404, detail=f"The post of id {id} is not found")
    
    if user_post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)  # pyright: ignore[reportArgumentType]
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    db.commit()

    return post_query.first()  