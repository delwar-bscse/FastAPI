from pydantic import BaseModel, HttpUrl, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Define request body schema.
class CourseCreate(BaseModel):
    name:str
    instructor:str
    duration:float
    website:HttpUrl

# Define response body schema.
class CourseResponse(CourseCreate):
    id:int
    creator_id:int
    model_config = ConfigDict(from_attributes=True)

# Define request body schema.
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    access_token:str
    user: UserResponse

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None