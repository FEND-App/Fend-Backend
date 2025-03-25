from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Annotated
import models
from models import User
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.get("/users/")
def get_users(db: db_dependency):
    users = db.query(User.id_user, User.username, User.is_active).all()
    return [{"id_user": User.id, "name": User.username, "Active": User.is_active} for User in users]