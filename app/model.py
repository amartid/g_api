# app/model.py

from pydantic import BaseModel

class PostSchema(BaseModel):
    title: str
    text: str
    
    # No need to include owner_id here since it will be assigned automatically

class UserSchema(BaseModel):
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str
