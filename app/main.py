from cachetools.func import ttl_cache
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models
from . import schemas
from . import utils
from .database import get_db, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)  # Create database schema
CACHE_TTL = 300  # Define the TTL (time-to-live) for caching in seconds (5 minutes)


@app.post("/signup/", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = utils.pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"access_token": utils.create_access_token(data={"sub": user.email}), "token_type": "bearer"}


@app.post("/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = utils.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/addPost/", response_model=schemas.PostID)
def add_post(post: schemas.PostCreate, current_user: models.User = Depends(utils.get_current_user),
             db: Session = Depends(get_db)):
    db_post = models.Post(text=post.text, user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"id": db_post.id}


@app.get("/getPosts/", response_model=list[schemas.PostInDB])
@ttl_cache(maxsize=128, ttl=CACHE_TTL)
def get_posts(current_user: models.User = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Post).filter(models.Post.user_id == current_user.id).all()


@app.delete("/deletePost/{post_id}/", response_model=dict)
def delete_post(post_id: int, current_user: models.User = Depends(utils.get_current_user),
                db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id,
                                           models.Post.user_id == current_user.id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
