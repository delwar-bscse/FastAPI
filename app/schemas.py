from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime

# Define request body schema.
class CourseCreate(BaseModel):
    name:str
    instructor:str
    duration:float
    website:HttpUrl

# Define response body schema.
class CourseResponse(CourseCreate):
    id:int
    class Config:
        orm_model = True

# Define request body schema.
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_model = True