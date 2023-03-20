from fastapi import FastAPI, status as STATUS, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from database import SessionLocal
from sqlalchemy import or_

import models

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Bookmark(BaseModel):
    id:int  
    owner_id: str
    url:str 
    private:bool
    class Config:
        orm_mode = True

class User(BaseModel):
    id:int   
    email:str   
    password:str
    token:str
    class Config:
        orm_mode = True

class BookmarkCreate(BaseModel):
    url: str
    private: bool

class UserCreate(BaseModel):
    email: str
    password: str

db = SessionLocal()

def find_user_by_token(token:str) -> int:
    user = db.query(models.User).filter(models.User.token == token).first()
    if not user:
        return None
    else:
        return user
@app.get('/health', response_model=Dict)
async def health():
    return {'health':'OK'}

@app.post('/register', response_model=Dict)
async def register_user(data: UserCreate):
    """
    Register user
    """
    token = data.email+'$123'
    #password needes to be salted, but keeping it simple for now.
    new_user = models.User(email=data.email, password=data.password, token=token)
    db.add(new_user)
    db.commit()
    return {'token':token}

@app.post('/login', response_model=Dict)
async def register_user(data: UserCreate):
    """
    Login user
    """
    #password needes to be salted, but keeping it simple for now.
    res = db.query(models.User).filter(models.User.email == data.email, models.User.password==data.password).first()
    if not res:
        raise HTTPException(status_code=STATUS.HTTP_401_UNAUTHORIZED, detail="Wrong Username or Password")
    return {'token':res.token}

@app.get('/bookmarks', 
    response_model = List[Bookmark],
    status_code = 200
    )
async def get_all_bookmarks(request: Request):
    token = request.headers.get('Authorization', None)
    if not token:
        raise HTTPException(status_code=STATUS.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    user = find_user_by_token(token)
    
    if user:
        bookmarks = db.query(models.Bookmark).filter(or_(models.Bookmark.private==False, models.Bookmark.owner_id == user.id)).all()
        if bookmarks:
            return bookmarks
        else:
            return []

@app.post('/bookmarks',
        response_model = Bookmark,
        status_code = STATUS.HTTP_201_CREATED
        )
async def create_a_bookmark(request: Request, _bookmark:BookmarkCreate):
    token = request.headers.get('Authorization', None)
    if not token:
        raise HTTPException(status_code=STATUS.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    user = find_user_by_token(token)
    if user:
        new_bookmark = models.Bookmark(owner_id=user.id, url = _bookmark.url, private=_bookmark.private)

        db.add(new_bookmark)
        db.commit()
        return new_bookmark
    else:
        raise HTTPException(status_code=STATUS.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")



@app.delete('/bookmarks/{bookmark_id}', response_model=Dict)
async def delete_bookmark(request: Request, bookmark_id:int):
    
    token = request.headers.get('Authorization', None)
    if not token:
        raise HTTPException(status_code=STATUS.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")
    
    bookmark_to_delete = db.query(models.Bookmark).filter(models.Bookmark.id==bookmark_id).first()
    if bookmark_to_delete is None:
        raise HTTPException(status_code=STATUS.HTTP_404_NOT_FOUND, detail="Resource Not Found")
    
    owner = db.query(models.User).filter(models.User.token == request.headers.get('Authorization')).first()
    if owner and bookmark_to_delete.owner_id == owner.id:    
        db.delete(bookmark_to_delete)
        db.commit()
    return {'success':'ok'}