from pydantic import BaseModel, HttpUrl

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