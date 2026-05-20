from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


# Define request body schema.
class Course(BaseModel):
    name:str
    instructor:str
    duration:float
    website:HttpUrl

@app.post("/post")
def create_post(post:Course):
    return post

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/course")
def read_root():
    return {"title": "FastAPI"}