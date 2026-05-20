from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)


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
    cursor.execute("SELECT * FROM course")
    data = cursor.fetchall()
    return {"data": data}

@app.get("/course")
def read_root():
    return {"title": "FastAPI"}